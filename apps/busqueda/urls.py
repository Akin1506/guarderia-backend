from django.urls import path
from .views import BusquedaGlobalView

urlpatterns = [
    path("", BusquedaGlobalView.as_view(), name="busqueda-global"),
]