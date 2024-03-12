from django.urls import path
from .views import OrderGenericAPIView, ExportCsvAPIView, ChartAPIView

urlpatterns = [
    path('get/orders/', OrderGenericAPIView.as_view()),
    path('order/<int:pk>/', OrderGenericAPIView.as_view()),
    path('export/csv/', ExportCsvAPIView.as_view()),
    path('chart/', ChartAPIView.as_view()),
]

