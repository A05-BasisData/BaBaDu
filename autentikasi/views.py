from django.shortcuts import render
from autentikasi.forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

def start_page(request):
    return render (request, 'landingPage.html')

def register(request):
    return render (request, 'register.html')

def login(request):
    return render (request, 'login.html')

def regist_atlet(request):
    form = regist_form_atlet

    if request.method == "POST":
        form = regist_form_atlet(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anda berhasil mendaftar sebagai atlet!')
            return redirect('autentikasi:login')

    context = {'form':form}
    return render(request, 'registerAtlet.html', context)

def regist_pelatih(request):
    form = regist_form_pelatih

    if request.method == "POST":
        form = regist_form_pelatih(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anda berhasil mendaftar sebagai pelatih!')
            return redirect('autentikasi:login')
    
    context = {'form':form}
    return render(request, 'registerPelatih.html', context)

def regist_umpire(request):
    form = regist_form_umpire

    if request.method == "POST":
        form = regist_form_umpire(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anda berhasil mendaftar sebagai umpire!')
            return redirect('autentikasi:login')
    
    context = {'form':form}
    return render(request, 'registerUmpire.html', context)

def login(request):
    # skip authentication
    username = request.POST.get('username')
    email = request.POST.get('email')
    return render(request, 'login.html')

    