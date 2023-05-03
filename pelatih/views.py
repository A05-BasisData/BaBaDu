from django.shortcuts import render

def dashboard_pelatih(request):
    return render (request, 'dashboardPelatih.html')

def daftar_atlet(request):
    return render (request, 'daftarAtlet.html')

def list_atlet(request):
    return render (request, 'listAtlet.html')
