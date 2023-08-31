from django.urls import path
from .views import UpdateDataViewSet

urlpatterns = [
    path('update-data/', UpdateDataViewSet.as_view({'get': 'update_data'}), name='update-data'),
]
