from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, viewsets, status
from users.models import MyUser, Role, Permission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer
from .authentication import generate_access_token,JWTAuthentication
from rest_framework.permissions import IsAuthenticated



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
    """This class handles user login"""
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = MyUser.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        if not user.is_password_valid(password):
           raise exceptions.AuthenticationFailed('Password is incorrect!')

        response = Response()
        token = generate_access_token(user)
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class AuthenticatedUser(APIView):
    """This class returns the authenticated user's data"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'data': serializer.data
        })


class LogOutView(APIView):
    """This class deletes the authorization token from the cookie."""
    def post(self,_):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'logout is success!'
        }
        return response


class PermissionView(APIView):
    """The class returns a list of serialized data - all permissions for users"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })


class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = RoleSerializer(Role.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })

    def create(self, request):
       serializer = RoleSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response({
           'data': serializer.data
       }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(role)

        return Response({
            'data': serializer.data
        })
    def update(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(instance=role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data
        }, status=status.HTTP_202_ACCEPTED)
    def destroy(self, request, pk=None):
        role = Role.objects.get(id=pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







