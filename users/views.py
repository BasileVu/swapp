import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsUserHimself, IsOwner
from users.serializers import *


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


@login_required(login_url="users:login", redirect_field_name="")
def account_view(request):
    return render(request, "users/account.html", {"username": request.user.username})

@require_GET
@login_required()
def get_personal_account_info(request):
    return JsonResponse({"username": request.user.username})


@require_POST
def api_login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data["username"]
        password = data["password"]
    except KeyError:
        return JsonResponse({"error": "a value is incorrect"}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse()
    else:
        return JsonResponse({"error": "invalid username/password combination"}, status=401)


@require_GET
@login_required()
def api_logout(request):
    logout(request)
    return HttpResponse()


# FIXME or delete
"""class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**request.data)
        response = Response(status=status.HTTP_201_CREATED)
        response['Location'] = "/api/users/%d/" % user.id
        return response"""


class UsersAccounts(APIView):
    # TODO delete if not used
    """def get(self, request):
        # A discuter si besoin ou non d'être connecté si on fait un get sur tous les user a la fois
        if not request.user.is_authenticated():
            return JsonResponse({"error": "you are not connected"}, status=status.HTTP_403_FORBIDDEN)
        # A compléter

        return JsonResponse({}, status=status.HTTP_200_OK)"""

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
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
        return response


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def user_account(request, pk):
    pk = int(pk)
    if request.user.id == pk:
        user = User.objects.get(pk=pk)
        user_profile = user.userprofile

        # TODO write serializer
        return Response(status=status.HTTP_200_OK, data={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "categories": [c.id for c in user_profile.categories.all()],  # FIXME
            "items": [i.id for i in user_profile.item_set.all()],  # FIXME
            "notes": [n.id for n in user_profile.note_set.all()],  # FIXME
            "likes": [l.id for l in user_profile.like_set.all()],  # FIXME
            "account_active": user_profile.account_active
        })
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserName(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserNameSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsUserHimself,)


class UserFirstName(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserFirstNameSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsUserHimself,)


class UserLastName(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLastNameSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsUserHimself,)


class UserEmail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserEmailSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsUserHimself)


class UserPassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsUserHimself,)


# Réfléchir à un meilleur moyen de faire l'activation d'un compte.
class UserProfileAccountActive(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileAccountActiveSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner,)
