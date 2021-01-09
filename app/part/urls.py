from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from part import views

app_name = 'part'

urlpatterns = [
    url(r'aggregated_data', views.AggregatedDataView.as_view()),
]

router = DefaultRouter()
router.register(r'data', views.PartViewSet, basename='data')
router.register(r'filters', views.FiltersViewSet, basename='filters')

urlpatterns += router.urls
