from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import AuthTokenSerializer


class CreateTokenView(ObtainAuthToken):
    """Принимает имя пользователя и пароль, возвращает токен для доступа к основному API """
    serializer_class = AuthTokenSerializer
