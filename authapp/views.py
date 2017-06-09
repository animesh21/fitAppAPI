from rest_framework import generics, permissions

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import Http404

from .serializers import UserSerializer


class UserListView(generics.ListCreateAPIView):
    """
    lists all the users and creates new ones. Also resets password 
    for users.
    """
    permission_classes = (permissions.AllowAny, )

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Gives detail of a particular user, updates and deletes as well.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


