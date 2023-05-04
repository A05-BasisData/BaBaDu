from django.shortcuts import render

def dashboard_umpire(request):
    return render (request, 'dashboardUmpire.html')

def lihat_event(request):
    return render (request, 'listEvent.html')

def pertandingan(request):
    return render (request, 'pertandingan.html')

def hasil_pertandingan(request):
    return render (request, 'hasilPertandingan.html')
