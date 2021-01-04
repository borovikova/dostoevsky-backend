from django.urls import path
from rest_framework.routers import DefaultRouter

from part import views


app_name = 'part'

router = DefaultRouter()
router.register(r'data', views.PartViewSet, basename='data')
router.register(r'filters', views.FiltersViewSet, basename='filters')
router.register(r'aggregated_data', views.AggregatedDataViewSet, basename='aggregated_data')
urlpatterns = router.urls

# urlpatterns = [
#     path('data/', views.PartViewSet.as_view({'get': 'list'}), name='data'),
#     path('filters/', views.FiltersViewSet.as_view(), name='filters'),
#     path('aggregated_data/', views.AggregatedDataViewSet.as_view({'get': 'list'}), name='aggregated_data'),
# ]
