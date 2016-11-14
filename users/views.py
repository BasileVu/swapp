import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# TODO delete when not used anymore
from users.models import UserProfile
from users.serializers import UserAccountSerializer


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


@api_view(['POST'])
def create_user(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data["username"]
        email = data["email"]
        password = data["password"]
    except KeyError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e) + " is incorrect"})

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
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e) + " is incorrect"})

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        print(User.objects.get(pk=1).username)
        print(User.objects.get(pk=1).password)
        print(username)
        print(password)
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "invalid username/password combination"})


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def logout_user(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


"""class UserAccount(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_profile = request.user.userprofile

        return Response(status=status.HTTP_200_OK, data={
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "account_active": user_profile.account_active,
            "last_modification_date": user_profile.last_modification_date,
            "categories": [c.id for c in user_profile.categories.all()],
            "items": [i.id for i in user_profile.item_set.all()],
            "notes": [n.id for n in user_profile.note_set.all()],
            "likes": [l.id for l in user_profile.like_set.all()],
        })

    def patch(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            username = data.get("username", None)
            password = data.get("password", None)
            first_name = data.get("first_name", None)
            last_name = data.get("last_name", None)
            email = data.get("email", None)
            account_active = data.get("account_active", None)


            username = data["username"]
            email = data["email"]
            password = data["password"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "a value is incorrect"})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)

        response = Response(status=status.HTTP_201_CREATED)
        response["Location"] = "/api/users/%d/" % user.id
        return response"""


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
            "account_active": user_profile.account_active,
            "last_modification_date": user_profile.last_modification_date,
            "categories": [c.id for c in user_profile.categories.all()],
            "items": [i.id for i in user_profile.item_set.all()],
            "notes": [n.id for n in user_profile.note_set.all()],
            "likes": [l.id for l in user_profile.like_set.all()],
        })


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def change_password(request):
    """
    An endpoint for changing password.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
        old_password = data["old_password"]
        password = data["password"]
    except KeyError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e) + " is incorrect"})

    # Check old password
    if not request.user.check_password(old_password):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"old_password": "Wrong password."}, )
    # set_password also hashes the password that the user will get
    self.object.set_password(serializer.data.get("new_password"))
    self.object.save()
    return Response("Success.", status=status.HTTP_200_OK)


# TODO delete
# class UserAccount(OwnUserMixin, generics.RetrieveAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserAccountSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class UserName(OwnUserMixin, generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserNameSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class UserFirstName(OwnUserMixin, generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserFirstNameSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class UserLastName(OwnUserMixin, generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserLastNameSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class UserEmail(OwnUserMixin, generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserEmailSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class UserPassword(OwnUserMixin, generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserPasswordSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# # Réfléchir à un meilleur moyen de faire l'activation d'un compte.
# class UserProfileAccountActive(OwnUserMixin, generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserProfileAccountActiveSerializer
#     permission_classes = (permissions.IsAuthenticated,)
