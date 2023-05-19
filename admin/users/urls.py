from django.urls import path
from .views import TestViews, RegisterViews, LoginView, AuthenticatedUser

urlpatterns = [
    path('all/', TestViews.as_view()),
    path('register/', RegisterViews.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', AuthenticatedUser.as_view()),
]
