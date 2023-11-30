from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, viewsets, status, generics, mixins
from admin.pagination import CustomPagination
from users.models import MyUser, Role, Permission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer
from .authentication import generate_access_token,JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import ViewPermissions


class TestViews(APIView):
    """This class returns all users from the database"""
    def get(self, request):
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



class RegisterViews(APIView):
    """This class handles the registration of new users"""
    def post(self, request):
        data = request.data
        data['role']=1
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
        # response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class AuthenticatedUser(APIView):
    """This class returns the authenticated user's data"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = UserSerializer(request.user).data
        data['permissions']=[p['name'] for p in data['role']['permissions']]
        return Response({
            'data': data
        })


class LogOutView(APIView):
    """This class deletes the authorization token from the cookie."""
    def post(self,request):
        token = request.data.get('removetoken')
        if token:
            response = Response()
            response.data = {
            'message': 'logout is success!'}
            return response




class PermissionView(APIView):
    """The class returns a list of serialized data - all permissions for users"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]

    def get(self, request):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })


class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_object = 'roles'

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



class UserGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """This class provides generic CRUD operations with objects of the MyUser model"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'users'
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })
        return self.list(request)

    def post(self, request):
        request.data.update({
            'password': 1234,
            'role': request.data['role_id']
        })
        return Response({
            'data': self.create(request).data
        })

    def put(self, request, pk=None):
        if request.data['role_id']:
            request.data.update({
                'password': 1234,
                'role': request.data['role_id']
            })

            return Response({
            'data': self.partial_update(request).data
        })

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class ProfileAPIView(APIView):
    """This class handles profile updates for a user"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    """This class manages password changes for a user"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,pk=None):
        user = request.user
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError("Password don't match")
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




