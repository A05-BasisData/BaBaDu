from django.shortcuts import render
from autentikasi.forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from utility.query import query
import uuid

def start_page(request):
    return render (request, 'landingPage.html')

def get_role(email):
    check_atlet = query(f"""SELECT * FROM MEMBER M JOIN ATLET A ON M.ID = A.ID WHERE M.Email = '{email}'""")
    check_pelatih = query(f"""SELECT * FROM MEMBER M JOIN PELATIH P ON M.ID = P.ID WHERE M.Email = '{email}'""")
    check_umpire = query(f"""SELECT * FROM MEMBER M JOIN UMPIRE U ON M.ID = U.ID WHERE M.Email = '{email}'""")

    if check_atlet != []:
        return "atlet"
    if check_pelatih != []:
        return "pelatih"
    if check_umpire != []:
        return "umpire"

def is_authenticated(request):
    try:
        request.session["email"]
        return True
    except KeyError:
        return False

def get_session_data(request):
    if not is_authenticated(request):
        return {}
    try:
        return {"email": request.session["email"], "role": request.session["role"]}
    except:
        return {}

def register(request):
    return render (request, 'register.html')

def login(request):
    next = request.GET.get("next")
    if is_authenticated(request):
        role = get_role(request.session["email"])
        if role == "atlet":
            return redirect("/dashboard/atlet")
        if role == "pelatih":
            return redirect("/dashboard/pelatih")
        if role == "umpire":
            return redirect("/dashboard/umpire")
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        check_member = query(f"""SELECT * FROM MEMBER WHERE nama='{nama}' and email='{email}'""")
        flag = is_authenticated(request)
        if check_member != [] and not flag:
            request.session["nama"] = nama
            request.session["email"] = email
            request.session["role"] = get_role(email)
            request.session.set_expiry(500)
            request.session.modified = True
            if next != None and next != "None":
                return redirect(next)
            else:
                role = get_role(email)
                if role == "atlet":
                    return redirect("/dashboard/atlet")
                if role == "pelatih":
                    return redirect("/dashboard/pelatih")
                if role == "umpire":
                    return redirect("/dashboard/umpire")   
    return render (request, 'login.html')

def regist_atlet(request):
    # form = regist_form_atlet

    if request.method == "POST":
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        play = request.POST.get('play')
        tinggi_badan = request.POST.get('tinggi_badan')
        jenis_kelamin = "Laki-Laki" if request.POST.get('jenis_kelamin') == True else "Perempuan"
    
        check_email = query(f"""SELECT * FROM MEMBER WHERE email = {email}""")
        if check_email == []:
            query(f"""INSERT INTO MEMBER VALUES ('{uuid.uuid1()}','{nama}', '{email}')""")
            query(f"""INSERT INTO ATLET VALUES ('{uuid.uuid1()}','{tanggal_lahir}', '{negara}', '{play}', '{tinggi_badan}', '{None}', '{jenis_kelamin}')""")
            return redirect('/login/')
        
        context = {'message': "Email sudah pernah terdaftar"}
        return render(request, "registerAtlet.html", context)
    
    context = {'message': ""}
    return render(request, "registerAtlet.html", context)
    #     form = regist_form_atlet(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Anda berhasil mendaftar sebagai atlet!')
    #         return redirect('autentikasi:login')

    # context = {'form':form}
    # return render(request, 'registerAtlet.html', context)

def regist_pelatih(request):
    # form = regist_form_pelatih

    if request.method == "POST":
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        kategori = request.POST.get('kategori')
        tanggal_mulai = request.POST.get('tanggal_mulai')
        
        check_email = query(f"""SELECT * FROM MEMBER WHERE email = {email}""")
        if check_email == []:
            query(f"""INSERT INTO MEMBER VALUES ('{uuid.uuid1()}','{nama}', '{email}')""")
            query(f"""INSERT INTO PELATIH VALUES ('{uuid.uuid1()}','{tanggal_mulai}')""")
            return redirect('/login/')
        
        context = {'message': "Email sudah pernah terdaftar"}
        return render(request, "registerPelatih.html", context)
    
    context = {'message': ""}
    return render(request, "registerPelatih.html", context)

    #     form = regist_form_pelatih(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Anda berhasil mendaftar sebagai pelatih!')
    #         return redirect('autentikasi:login')
    
    # context = {'form':form}
    # return render(request, 'registerPelatih.html', context)

def regist_umpire(request):
    # form = regist_form_umpire

    if request.method == "POST":
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        
        check_email = query(f"""SELECT * FROM MEMBER WHERE email = {email}""")
        if check_email == []:
            query(f"""INSERT INTO MEMBER VALUES ('{uuid.uuid1()}','{nama}', '{email}')""")
            query(f"""INSERT INTO UMPIRE VALUES ('{uuid.uuid1()}','{negara}')""")
            return redirect('/login/')
        
        context = {'message': "Email sudah pernah terdaftar"}
        return render(request, "registerUmpire.html", context)
    
    context = {'message': ""}
    return render(request, "registerUmpire.html", context)
    #     form = regist_form_umpire(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Anda berhasil mendaftar sebagai umpire!')
    #         return redirect('autentikasi:login')
    
    # context = {'form':form}
    # return render(request, 'registerUmpire.html', context)

# def login(request):
#     # skip authentication
#     username = request.POST.get('username')
#     email = request.POST.get('email')
#     return render(request, 'login.html')

    