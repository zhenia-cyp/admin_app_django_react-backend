from django.urls import path
from users.views import *


urlpatterns = [
    path('test/', TestViews.as_view()),
]
