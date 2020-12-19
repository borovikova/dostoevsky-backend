from django.urls import path

from part import views


app_name = 'part'

urlpatterns = [
    path('data/', views.PartViewSet.as_view({'get': 'list'}), name='data'),
    path('filters/', views.FiltersViewSet.as_view(), name='filters'),
]
