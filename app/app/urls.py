from django.contrib import admin
from django.urls import path, re_path, include

from django.views.generic import TemplateView

from . import views


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
