from django.urls import path
from umpire.views import *

app_name = 'umpire'

urlpatterns = [
    path('', dashboard_umpire, name = 'dashboard_umpire'),
    path('dashboard/', dashboard_umpire, name = 'dashboard_umpire'),
    path('list_event/', lihat_event, name = 'lihat_event'),
    path('pertandingan/<str:prtdg>/', pertandingan, name = 'pertandingan'),
    path('hasil_pertandingan/<str:nama_event>/<int:tahun>/', hasil_pertandingan, name = 'hasil_pertandingan'),
    path('lihat_atlet/', lihat_atlet, name = 'lihat_atlet'),
]