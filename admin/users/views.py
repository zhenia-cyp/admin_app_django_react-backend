from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from users.models import User
from .serializers import UserSerializer


class TestViews(APIView):

    def get(self,request):
        users = User.objects.all()
        return Response(users)


class RegisterViews(APIView):

    def post(self,request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match')
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)