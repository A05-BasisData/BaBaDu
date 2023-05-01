from django.urls import path
from autentikasi.views import *

app_name = 'autentikasi'

urlpatterns = [
    path('', start_page, name = 'start_page'),
    path('register/', register, name = 'register'),
    path('login/', login, name = 'login'),
    path('register/atlet', regist_atlet, name = 'regist_atlet'),
    path('register/pelatih', regist_pelatih, name = 'regist_pelatih'),
    path('register/umpire', regist_umpire, name = 'regist_umpire')
]