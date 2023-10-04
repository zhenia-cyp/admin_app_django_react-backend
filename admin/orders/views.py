from rest_framework import generics, mixins
from users.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from admin.pagination import CustomPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import csv




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



class ExportCsvAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'

        orders = Order.objects.all()
        writer = csv.writer(response)

        writer.writerow(['ID', 'Name', 'Email', 'Product Title', 'Price', 'Quantity'])

        for order in orders:
            writer.writerow([order.id, order.name, order.email, '', '', ''])
            orderItems = OrderItem.objects.all().filter(order_id=order.id)

            for item in orderItems:
                writer.writerow(['', '', '', item.product_title, item.price, item.quantity])

        return response
