from django.shortcuts import render, redirect
from utility.query import query
from django.http import HttpResponse
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
    if request.method == 'GET':
        atlet = {}
        atlet['atlet'] = [atlet._asdict() for atlet in query(
        f'''SELECT M.id, M.nama FROM ATLET A JOIN MEMBER M ON M.id = A.id'''
        )]
        return render (request, 'daftarAtlet.html', {'data_atlet':atlet})
    
    elif request.method == 'POST':
        id_pelatih = '4e3f8ae6-1004-48cc-afb7-e6df8340cadd'
        nama_atlet = request.POST.get('nama_atlet')

        # print(nama_atlet)
        id_atlet = query(
            f'''SELECT M.id FROM MEMBER M
            WHERE M.nama = '{nama_atlet}'
            '''
        )
        # print(id_atlet)
        
        print(query(
            f'''INSERT INTO ATLET_PELATIH VALUES(
                '{id_pelatih}', '{id_atlet[0].id}'
                )
            '''
        ))

        # query(f'''INSERT INTO ATLET_PELATIH VALUES('{id_pelatih}', '{id_atlet}') ''')
        return redirect('pelatih:list_atlet')
        

def list_atlet(request):
    # id_pelatih = request.user.member.id
    id_pelatih = '4e3f8ae6-1004-48cc-afb7-e6df8340cadd'
    atlet_dilatih = {}
    atlet_dilatih['atlet_dilatih'] = [atlet_dilatih._asdict() for atlet_dilatih in query(
        f'''SELECT M.nama, M.email, A.world_rank FROM ATLET_PELATIH AP JOIN ATLET A ON AP.id_atlet = A.id 
        JOIN MEMBER M ON A.id = M.id WHERE AP.ID_Pelatih = '{id_pelatih}' '''
    )]
    
    # print(atlet_dilatih)
    return render (request, 'listAtlet.html', {'data_atlet':atlet_dilatih})
