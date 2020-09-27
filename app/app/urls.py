from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions, status
from rest_framework.schemas import get_schema_view

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema

from . import views, serializers

from django.views.generic import TemplateView

urlpatterns = [
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('api/', include('part.urls')),
]

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Dostoevsky API",
#         default_version='v1',
#         description="Доступ к данным для проекта Достоевский",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# username = openapi.Parameter('username', openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING)
# password = openapi.Parameter('password', openapi.IN_QUERY, description="password", type=openapi.TYPE_STRING)

# decorated_auth_view = \
#    swagger_auto_schema(
#       method='post',
#       responses={status.HTTP_200_OK: serializers.AuthTokenSerializer},
#      request_body=openapi.Schema(
#     type=openapi.TYPE_OBJECT, 
#     properties={
#         'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#         'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#     }
# )
#    )(views.CreateTokenView.as_view())

# urlpatterns = [
#     path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('admin/', admin.site.urls),
#     path('token/', decorated_auth_view, name='token'), # views.CreateTokenView.as_view()
#     path('api/', include('part.urls')),
# ]
