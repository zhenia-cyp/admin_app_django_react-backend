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