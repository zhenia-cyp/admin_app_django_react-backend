from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User


class TestViews(APIView):

    def get(self, request):
        users = User.objects.all()
        return Response(users)

