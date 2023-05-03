from django.urls import path
from pelatih.views import *

app_name = 'pelatih'

urlpatterns = [
    path('', dashboard_pelatih, name = 'dashboard_pelatih'),
    path('dashboard/', dashboard_pelatih, name = 'dashboard_pelatih'),
    path('daftar_atlet/', daftar_atlet, name = 'daftar_atlet'),
    path('list_atlet/', list_atlet, name = 'list_atlet'),
]