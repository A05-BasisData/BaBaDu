from django.shortcuts import render
from autentikasi.forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from utility.query import query
import uuid

def start_page(request):
    return render (request, 'landingPage.html')

def get_role(id):
    check_atlet = query(f"""SELECT * FROM ATLET WHERE id = '{id}'""")
    check_pelatih = query(f"""SELECT * FROM PELATIH WHERE id = '{id}'""")
    check_umpire = query(f"""SELECT * FROM UMPIRE WHERE id = '{id}'""")

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
            return redirect("atlet:dashboard_atlet")
        if role == "pelatih":
            return redirect("pelatih:dashboard_pelatih")
        if role == "umpire":
            return redirect("umpire:dashboard_umpire")
    if request.method == 'POST':
        nama = request.POST.get('username')
        email = request.POST.get('email')
        check_member = query(f"""SELECT id FROM MEMBER WHERE nama='{nama}' and email='{email}'""")
        print("ini check member")
        print(check_member)
        flag = is_authenticated(request)
        if check_member != [] and not flag:
            request.session["nama"] = nama
            request.session["email"] = email
            request.session["role"] = get_role(check_member[0].id)
            request.session["id"] = str(check_member[0].id)
            request.session.set_expiry(500)
            request.session.modified = True
            if next != None and next != "None":
                return redirect(next)
            else:
                role = get_role(check_member[0].id)
                if role == "atlet":
                    return redirect("atlet:dashboard_atlet")
                if role == "pelatih":
                    return redirect("pelatih:dashboard_pelatih")
                if role == "umpire":
                    return redirect("umpire:dashboard_umpire")   
    return render (request, 'login.html')

def regist_atlet(request):
    # form = regist_form_atlet
    myuuid = uuid.uuid1()
    if request.method == "POST":
        nama = request.POST.get('username')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        play = request.POST.get('play')
        tinggi_badan = request.POST.get('tinggi_badan')
        jenis_kelamin = request.POST.get('jenis_kelamin')


        check_email = query(f"""SELECT * FROM MEMBER WHERE email = '{email}'""")
        if isinstance(check_email, Exception):
            trigger_msg = check_email.args[0].split("\n")[0]
            messages.error(request, trigger_msg)
            return redirect("/register/atlet")
        if check_email == []:
            print(query(f"""INSERT INTO MEMBER VALUES ('{myuuid}','{nama}', '{email}')"""))
            print(query(f"""INSERT INTO ATLET (id, tgl_lahir, negara_asal, play_right, height, jenis_kelamin)
                            VALUES ('{myuuid}','{tanggal_lahir}', '{negara}', '{play}', '{tinggi_badan}', '{jenis_kelamin}')"""))
            print(query(f"""INSERT INTO ATLET_NON_KUALIFIKASI VALUES ('{myuuid}')"""))
            return redirect('/login/')
        else:
            context = {'message': "Email sudah pernah terdaftar"}
            return render(request, "registerAtlet.html", context)
    
    context = {'message': ""}
    return render(request, "registerAtlet.html", context)


def regist_pelatih(request):
    # form = regist_form_pelatih
    myuuid = uuid.uuid1()
    if request.method == "POST":
        nama = request.POST.get('username')
        email = request.POST.get('email')
        spesialisasi = {
            "tunggal_putra":request.POST.get('spesialisasi1'),
            "tunggal_putri":request.POST.get('spesialisasi2'),
            "ganda_putra":request.POST.get('spesialisasi3'),
            "ganda_putri":request.POST.get('spesialisasi4'),
            "ganda_campuran":request.POST.get('spesialisasi5')
        }
        tanggal_mulai = request.POST.get('tanggal_mulai')

        id_spesialisasi = {
            "tunggal_putra":str(query("SELECT S.id FROM spesialisasi S WHERE S.spesialisasi = 'Tunggal Putra';")[0].id),
            "tunggal_putri":str(query("SELECT S.id FROM spesialisasi S WHERE S.spesialisasi = 'Tunggal Putri';")[0].id),
            "ganda_putra":str(query("SELECT S.id FROM spesialisasi S WHERE S.spesialisasi = 'Ganda Putra';")[0].id),
            "ganda_putri":str(query("SELECT S.id FROM spesialisasi S WHERE S.spesialisasi = 'Ganda Putri';")[0].id),
            "ganda_campuran":str(query("SELECT S.id FROM spesialisasi S WHERE S.spesialisasi = 'Ganda Campuran';")[0].id)
        }
        
        check_email = query(f"""SELECT * FROM MEMBER WHERE email = '{email}'""")
        if isinstance(check_email, Exception):
            trigger_msg = check_email.args[0].split("\n")[0]
            messages.error(request, trigger_msg)
            return redirect("/register/pelatih")
        if check_email == []:
            print(query(f"""INSERT INTO MEMBER VALUES ('{myuuid}','{nama}', '{email}')"""))
            print(query(f"""INSERT INTO PELATIH VALUES ('{myuuid}','{tanggal_mulai}')"""))
            for i in spesialisasi:
                if spesialisasi[i] is not None:
                    print(query(f"""INSERT INTO PELATIH_SPESIALISASI VALUES('{myuuid}', '{id_spesialisasi[i]}')"""))
            return redirect('/login/')
        else:
            context = {'message': "Email sudah pernah terdaftar"}
            return render(request, "registerPelatih.html", context)
    
    context = {'message': ""}
    return render(request, "registerPelatih.html", context)

def regist_umpire(request):
    # form = regist_form_umpire
    myuuid = uuid.uuid1()
    if request.method == "POST":
        nama = request.POST.get('username')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        
        check_email = query(f"""SELECT * FROM MEMBER WHERE email = '{email}'""")
        if isinstance(check_email, Exception):
            trigger_msg = check_email.args[0].split("\n")[0]
            messages.error(request, trigger_msg)
            return redirect("/register/umpire")
        if check_email == []:
            print(query(f"""INSERT INTO MEMBER VALUES ('{myuuid}','{nama}', '{email}')"""))
            print(query(f"""INSERT INTO UMPIRE VALUES ('{myuuid}','{negara}')"""))
            return redirect('/login/')
        else:
            context = {'message': "Email sudah pernah terdaftar"}
            return render(request, "registerUmpire.html", context)
        
    context = {'message': ""}
    return render(request, "registerUmpire.html", context)


def logout(request):
    next = request.GET.get("next")

    if not is_authenticated(request):
        return redirect("/")

    request.session.flush()
    request.session.clear_expired()

    if next != None and next != "None":
        return redirect(next)
    else:
        return redirect("/")

    