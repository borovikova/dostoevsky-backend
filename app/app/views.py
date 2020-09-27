from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from rest_framework.settings import api_settings

from .serializers import AuthTokenSerializer

# from drf_yasg.utils import swagger_auto_schema

# @swagger_auto_schema(method='post', auto_schema=None)
class CreateTokenView(ObtainAuthToken, APIView):
    """Принимает имя пользователя и пароль, возвращает токен для доступа к основному API """
    serializer_class = AuthTokenSerializer
