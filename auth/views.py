from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import generics, status, authentication, permissions
from rest_framework.views import APIView

from core.models import UserProfile
from .serializers import AuthTokenSerializer, RegisterSerializer, \
    UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


AUTH_ME = '''{
    "user": <user id>, 
    "wallet": <user wallet>,
    "name": <user name>,
    "address": <user address>,
}'''

class UserProfileAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description='return user profile details',
                         responses={200: AUTH_ME})

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
