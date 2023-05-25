from django.shortcuts import render, redirect
from utility.query import query

def dashboard_pelatih(request):
    return render (request, 'dashboardPelatih.html')

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
