from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.core.mail import send_mail
from django.views import View

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.send_mail import send_confirmation_email
from user.serializers import RegisterApiSerializer, LoginSerializer



User = get_user_model()

# Registration for users

class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_mail('Код для активации!',f"Активационный код: {user.activation_code}", 'ujumakadyrov2@gmail.com', [user.email])
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )



# Activation for user profile

class ActivationView(APIView):

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True

            user.activation_code = ''
            user.save()
            return Response({"message": "Successfully activated"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "No"}, status=status.HTTP_400_BAD_REQUEST)


#  Login for users

class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer