from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from swapp.gmaps_api_utils import get_coordinates
from users.serializers import *


# TODO delete when not user anymore
def register_view(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirmation = request.POST["password-confirmation"]
        email = request.POST["email"]
    except KeyError:
        return render(request, "users/register.html")

    if password != password_confirmation:
        return render(request, "users/register.html", {
            "error_message": "Passwords don't match."
        })

    try:
        user = User.objects.create_user(username, email, password)
    except IntegrityError:
        return render(request, "users/register.html", {
            "error_message": "User already exists."
        })

    login(request, user)
    return HttpResponseRedirect(reverse("users:account"))


# TODO delete when not used anymore
def login_view(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except KeyError:
        return render(request, "users/login.html")

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("users:account"))
    else:
        return render(request, "users/login.html", {
            "error_message": "Incorrect username/password combination."
        })


# TODO delete when not used anymore
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


# TODO delete when not used anymore
@login_required(login_url="users:login", redirect_field_name="")
def account_view(request):
    return render(request, "users/account.html", {"username": request.user.username})


class OwnUserAccountMixin:
    def get_object(self):
        return self.request.user


@api_view(["GET"])
@ensure_csrf_cookie
def get_csrf_token(request):
    return Response()


@api_view(["POST"])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user = User.objects.create_user(**serializer.validated_data)
    except IntegrityError:
        return Response(status=status.HTTP_409_CONFLICT, data="An user with the same username already exists")

    response = Response(status=status.HTTP_201_CREATED)
    response["Location"] = "/api/users/%d/" % user.id
    return response


@api_view(['POST'])
def login_user(request):
    serializer = LoginUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user is not None:
        login(request, user)
        return Response()
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "invalid username/password combination"})


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def logout_user(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class UserAccount(OwnUserAccountMixin, generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = request.user.userprofile

        return Response({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "location": LocationSerializer(user.location).data,
            "last_modification_date": user_profile.last_modification_date,
            "categories": [c.id for c in user_profile.categories.all()],
            "items": [i.id for i in user.item_set.all()],
            "notes": [n.id for n in user.note_set.all()],
            "likes": [l.id for l in user.like_set.all()],
        })

    def update(self, request, *args, **kwargs):
        new_username = request.data.get("username", None)
        if new_username is not None and User.objects.filter(username=new_username).count() > 0:
            return Response(status=status.HTTP_409_CONFLICT, data={"error": "An user with same name already exists"})
        return super(UserAccount, self).update(request, *args, **kwargs)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def change_password(request):
    """
    An endpoint for changing password.
    """
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    old_password = serializer.validated_data["old_password"]
    new_password = serializer.validated_data["new_password"]

    if not request.user.check_password(old_password):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"old_password": "wrong password"})

    request.user.set_password(new_password)
    request.user.save()
    return Response(status=status.HTTP_200_OK)


class LocationView(generics.UpdateAPIView):
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.location

    def perform_update(self, serializer):
        data = get_coordinates(Location(**serializer.validated_data))

        if len(data) == 0:
            raise ValidationError("Could not find any match for specified location.")

        u = self.request.user
        c = u.coordinates
        c.latitude = data[0]["lat"]
        c.longitude = data[0]["lng"]
        c.save()

        serializer.save()


@api_view(["GET"])
def get_public_account_info(request, username):
    user = get_object_or_404(User, username=username)

    return Response({
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "location": "%s, %s, %s" % (user.location.city, user.location.region, user.location.country),
        "items": [i.id for i in user.item_set.all()],
        "notes": user.note_set.count(),
    })


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return NoteUpdateSerializer
        return NoteSerializer

    def perform_create(self, serializer):
        # Will be done on every save

        serializer.is_valid(raise_exception=True)
        offer = serializer.validated_data["offer"]

        if offer.accepted is not True:
            raise ValidationError("You can't not make a note if the offer has not been accepted")
        if offer.item_given.owner == self.request.user:
            serializer.validated_data["user"] = offer.item_received.owner
        elif offer.item_received.owner == self.request.user:
            serializer.validated_data["user"] = offer.item_given.owner
        else:
            raise ValidationError("You are not linked to this offer")

        if Note.objects.filter(offer=offer, user=serializer.validated_data["user"]).count() > 0:
            raise ValidationError("You have already noted this offer")
        serializer.save()
