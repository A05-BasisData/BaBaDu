from django.urls import path
from atlet.views import *

app_name = 'atlet'

urlpatterns = [
    path('', dashboard_atlet, name = 'dashboard_atlet'),
    path('dashboard/', dashboard_atlet, name = 'dashboard_atlet'),
    path('tes_kualifikasi/', tes_kualifikasi, name = 'tes_kualifikasi'),
    path('pertanyaan_kualifikasi/', pertanyaan_kualifikasi, name = 'pertanyaan_kualifikasi'),
    path('daftar_event/<str:evname>/', daftar_event, name = 'daftar_event'),
    path('pilih_stadium/', pilih_stadium, name = 'pilih_stadium'),
    path('pilih_event/<str:stdname>/', pilih_event, name = 'pilih_event'),
    path('enrolled_event/', enrolled_event, name = 'enrolled_event'),
    path('daftar_sponsor/', daftar_sponsor, name = 'daftar_sponsor')
]