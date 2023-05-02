from django.urls import path
from pelatih.views import *

app_name = 'pelatih'

urlpatterns = [
    path('dashboard/', dashboard_pelatih, name = 'dashboard_pelatih'),

]