from django.urls import path
from .views import OrderGenericAPIView, ExportCsvAPIView

urlpatterns = [
    path('orders/', OrderGenericAPIView.as_view()),
    path('order/<str:pk>/', OrderGenericAPIView.as_view()),
    path('export/csv/', ExportCsvAPIView.as_view()),
]

