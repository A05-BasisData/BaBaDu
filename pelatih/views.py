from django.http import HttpResponse
from django.shortcuts import render
from autentikasi.views import *


def dashboard_pelatih(request):
    if not is_authenticated(request):
        return redirect('/login')
    
    if request.session["role"] != "pelatih":
        return HttpResponse("401 Unauthorized: Unauthorized session role Pelatih")
    
    pelatih_data = query(
        f'''SELECT pelatih.id, nama, email, tanggal_mulai FROM pelatih
            JOIN member m on m.id = pelatih.id
            WHERE m.nama = '{request.session["nama"]}' AND m.email = '{request.session["email"]}';
        '''
    )

    nama_lengkap = pelatih_data[0].nama
    email = pelatih_data[0].email
    spesialiasi = [std._asdict() for std in query(
        f'''SELECT spesialisasi FROM spesialisasi
            JOIN pelatih_spesialisasi ps on spesialisasi.id = ps.id_spesialisasi
            WHERE ps.id_pelatih = '{request.session["id"]}'
        '''
    )]
    tanggal_mulai = pelatih_data[0].tanggal_mulai

    context = {
        "Nama_Lengkap" : nama_lengkap,
        "Email" : email,
        "Spesialisasi" : spesialiasi,
        "Tanggal_Mulai" : tanggal_mulai,
    }
    print(context)
    return render (request, 'dashboardPelatih.html', context)

def daftar_atlet(request):
    return render (request, 'daftarAtlet.html')

def list_atlet(request):
    return render (request, 'listAtlet.html')
