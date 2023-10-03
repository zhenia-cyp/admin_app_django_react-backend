from rest_framework import generics, mixins
from users.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.response import Response
from admin.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage



class ProductGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    """This class handles crud operations for the Product model"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)

    def post(self, request):
        return Response({
            'data': self.create(request).data
        })

    def put(self, request, pk=None):
        return Response({
            'data': self.partial_update(request, pk).data
        })

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class FileUploadView(APIView):
    """The class uploads files to the media folder"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self,request):
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)
        return Response({
            'url': 'http://localhost:8000' + url
        })