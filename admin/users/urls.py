from django.urls import path
from .views import TestViews, RegisterViews, LoginView, AuthenticatedUser, LogOutView, PermissionView, RoleViewSet, \
    UserGenericAPIView

urlpatterns = [
    path('all/', TestViews.as_view()),
    path('register/', RegisterViews.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', AuthenticatedUser.as_view()),
    path('logout/', LogOutView.as_view()),
    path('permissions/', PermissionView.as_view()),
    path('roles/', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('roles/<int:pk>/', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('get/users/', UserGenericAPIView.as_view()),
    path('get/users/<int:pk>', UserGenericAPIView.as_view()),
]
