from rest_framework import generics, mixins
from users.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from orders.serializers import OrderSerializer
from admin.pagination import CustomPagination
from rest_framework.response import Response




class OrderGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """Class either retrieves a single order by its primary key or lists orders"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)
