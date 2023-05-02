from django.urls import path
from atlet.views import *

app_name = 'atlet'

urlpatterns = [
    path('dashboard/', dashboard_atlet, name = 'dashboard_atlet'),

]