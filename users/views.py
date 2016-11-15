import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from users.models import UserProfile
from users.serializers import UserAccountSerializer


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
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data["username"]
        email = data["email"]
        password = data["password"]
    except KeyError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "field " + str(e) + " is incorrect"})

    # Check if not empty fields
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "error": "fields '" + username + "' and '" + password + "' can't be empty"})

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
    except IntegrityError:
        return Response(status=status.HTTP_409_CONFLICT)

    response = Response(status=status.HTTP_201_CREATED)
    response["Location"] = "/api/users/%d/" % user.id
    return response


@api_view(['POST'])
def login_user(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data["username"]
        password = data["password"]
    except KeyError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "field " + str(e) + " is incorrect"})

    # Check if not empty fields
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "fields can't be empty"})

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "invalid username/password combination"})


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def logout_user(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class UserAccount(OwnUserAccountMixin, generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = request.user.userprofile

        return Response(status=status.HTTP_200_OK, data={
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "location": user_profile.location,
            "is_active": user.is_active,
            "last_modification_date": user_profile.last_modification_date,
            "categories": [c.id for c in user_profile.categories.all()],
            "items": [i.id for i in user_profile.item_set.all()],
            "notes": [n.id for n in user_profile.note_set.all()],
            "likes": [l.id for l in user_profile.like_set.all()],
        })

    # FIXME two errors occur when we launch the tests (two users can't have the same username)
    def update(self, request, *args, **kwargs):
        # FIXME improve that with direct serializer
        location = request.data.get("location")

        if location is not None:
            request.user.userprofile.location = location
            request.user.userprofile.save()

        try:
            return super(UserAccount, self).update(request, *args, **kwargs)
        except IntegrityError as e:
            return Response(status=status.HTTP_409_CONFLICT, data={"error": str(e)})


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def change_password(request):
    """
    An endpoint for changing password.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
        old_password = data["old_password"]
        new_password = data["new_password"]
    except KeyError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "field " + str(e) + " is incorrect"})

    # Check if not empty fields
    if not old_password or not new_password:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "fields can't be empty"})

    # Check old password
    if not request.user.check_password(old_password):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"old_password": "wrong password"})

    # set_password also hashes the password that the user will get
    request.user.set_password(new_password)
    request.user.save()
    return Response(status=status.HTTP_200_OK)
