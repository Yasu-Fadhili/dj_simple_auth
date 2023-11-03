from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import (
    views,
    authentication,
    permissions,
    response,
    generics
)
from rest_framework.authtoken.views import (
    ObtainAuthToken
)
from rest_framework.authtoken.models import (
    Token
)

from .serializers import UserSerializer


User = get_user_model()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = serializer.serializer_class(data=request.data,
                                                 context = {"resquest": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        
        return response.Response({
            "token": token.key,
            "user_id": user.pk,
            "username": user.username,
            "email": user.email
        })



class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class UserLoginView(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.auth.delete()
        return response.Response({'message': 'Logout successful'})



