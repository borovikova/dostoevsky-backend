from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('api/', include('part.urls')),
]
