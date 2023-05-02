from django.urls import path
from umpire.views import *

app_name = 'umpire'

urlpatterns = [
    path('dashboard/', dashboard_umpire, name = 'dashboard_umpire'),

]