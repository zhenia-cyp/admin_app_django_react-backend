from django.urls import path
from .views import TestViews,RegisterViews


urlpatterns = [
    path('all/', TestViews.as_view()),
    path('register/', RegisterViews.as_view()),
]
