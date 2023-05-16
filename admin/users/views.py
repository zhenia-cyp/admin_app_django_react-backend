from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from users.models import MyUser
from .serializers import UserSerializer



class TestViews(APIView):
    """This class returns all users from the database"""
    def get(self, request):
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterViews(APIView):
    """This class handles the registration of new users"""
    def post(self,request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match')
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = MyUser.objects.filter(email=email).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        if not user.is_password_valid(password):
           raise exceptions.AuthenticationFailed('Password is incorrect!')
        return Response('success!')