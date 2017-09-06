from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import authenticate
from django.contrib.auth import login, logout
from .serializers import UserSerializer
from .permissions import IsUserTheUpdater


class UserListView(generics.ListCreateAPIView):
    """
    lists all the users and creates new ones.
    """
    permission_classes = (permissions.AllowAny, )

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Gives detail of a particular user, updates and deletes as well.
    """

    permission_classes = (permissions.IsAuthenticated, IsUserTheUpdater)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):

    http_method_names = ['post', ]

    def post(self, request):
        data = request.data
        try:
            credentials = dict(username=data['username'], password=data['password'])
        except KeyError as e:
            data = {'message': 'username or password not present in the data.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(**credentials)
        if user:
            login(request, user)
            user_serializer = UserSerializer(user, context={'request': request})
            return Response(data=user_serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    http_method_names = ['get', ]

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        if request.user is not None:
            logout(request)
            return Response(data={'message': 'logout successful!'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'message': 'user was not logged in'}, status=status.HTTP_400_BAD_REQUEST)
