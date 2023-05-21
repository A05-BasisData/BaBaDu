from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from atlet.forms import *
from utility.query import query

def dashboard_atlet(request):
    return render (request, 'dashboardAtlet.html')

def tes_kualifikasi(request):
    return render (request, 'tesKualifikasi.html')

def pertanyaan_kualifikasi(request):
    return render (request, 'pertanyaanKualifikasi.html')

def pilih_stadium(request):
    cnt = query(f'''
        select count(*) from stadium;
    ''')
    print("jumlah stadium")
    print(cnt[0].count)

    cnt = query(f'''
        select * from stadium;
    ''')
    return render (request, 'pilihStadium.html')

def daftar_event(request):
    return render (request, 'daftarEventAtlet.html')

def pilih_event(request):
    return render (request, 'pilihEvent.html')

def enrolled_event(request):
    return render (request, 'enrolledEvent.html')

def daftar_sponsor(request):
    form = regist_sponsor

    if request.method == "POST":
        form = regist_sponsor(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anda berhasil mendaftar sebagai atlet!')
            return redirect('atlet:dashboard_atlet')
        
    context = {'form':form}
    return render(request, 'daftarSponsor.html', context)


