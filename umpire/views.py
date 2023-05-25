from django.shortcuts import render
from utility.query import query

def dashboard_umpire(request):
    return render (request, 'dashboardUmpire.html')

def lihat_atlet(request):
    atlet_kualifikasi = {}
    atlet_non_kualifikasi = {}
    
    atlet_kualifikasi['atlet_kualifikasi'] = [atlet_kualifikasi._asdict() for atlet_kualifikasi in query(
        f'''SELECT M.Nama, A.Tgl_Lahir, A.Negara_Asal, A.Play_Right, A.Height, A.World_Rank, AK.World_Tour_Rank, A.Jenis_Kelamin, PH.Total_Point
        FROM MEMBER M JOIN ATLET A ON M.ID = A.ID JOIN ATLET_KUALIFIKASI AK ON A.ID = AK.ID_Atlet 
        INNER JOIN (SELECT ID_Atlet, MAX(Total_Point) AS Total_Point FROM POINT_HISTORY GROUP BY ID_Atlet) PH ON A.ID = PH.ID_Atlet;
        '''
    )]

    atlet_non_kualifikasi['atlet_non_kualifikasi'] = [atlet_non_kualifikasi._asdict() for atlet_non_kualifikasi in query(
        f'''SELECT M.Nama, A.Tgl_Lahir, A.Negara_Asal, A.Play_Right, A.Height, A.World_Rank, A.Jenis_Kelamin
        FROM MEMBER M JOIN ATLET A ON M.ID = A.ID JOIN ATLET_NON_KUALIFIKASI ANK ON A.ID = ANK.ID_Atlet;
        '''
    )]

    query_atlet_ganda = query(
        f'''SELECT AG.ID_Atlet_Ganda, M1.Nama AS Nama_Atlet_Kualifikasi, M2.Nama AS Nama_Atlet_Kualifikasi_2, (PH1.Total_Point + PH2.Total_Point) AS Total_Point FROM Atlet_Ganda AG
        JOIN MEMBER M1 ON M1.ID = AG.ID_Atlet_Kualifikasi
        JOIN MEMBER M2 ON M2.ID = AG.ID_Atlet_Kualifikasi_2
        JOIN (SELECT ID_Atlet, MAX(Total_Point) AS Total_Point FROM POINT_HISTORY GROUP BY ID_Atlet) PH1 ON PH1.ID_Atlet = M1.ID
        JOIN (SELECT ID_Atlet, MAX(Total_Point) AS Total_Point FROM POINT_HISTORY GROUP BY ID_Atlet) PH2 ON PH2.ID_Atlet = M2.ID;
        '''
    )

    list_atlet_ganda = [
        {
            'id_atlet_ganda': ag.id_atlet_ganda,
            'nama_atlet_kualifikasi': ag.nama_atlet_kualifikasi,
            'nama_atlet_kualifikasi_2': ag.nama_atlet_kualifikasi_2,
            'total_point': ag.total_point
        }
        for ag in query_atlet_ganda
    ]

    atlet_ganda = {'atlet_ganda':list_atlet_ganda}

    context = {
        'data_ak':atlet_kualifikasi,
        'data_ank':atlet_non_kualifikasi,
        'data_ag':atlet_ganda
    }

    return render (request, 'listAtletUmpire.html', context)

def lihat_event(request):
    event = {}
    # Masih salah perlu sesuai dengan partai kompetisi
    event['event'] = [event._asdict() for event in query(
        f'''SELECT pk.nama_event, pk.tahun_event, e.nama_stadium, pk.jenis_partai, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, count(pme.nomor_peserta) as occupied, s.kapasitas FROM partai_kompetisi pk
        JOIN event e on pk.nama_event = e.nama_event and pk.tahun_event = e.tahun
        LEFT OUTER JOIN peserta_mendaftar_event pme on pme.nama_event = e.nama_event and pme.tahun = e.tahun
        JOIN stadium s on e.nama_stadium = s.nama
        GROUP BY pk.nama_event, pk.tahun_event, e.nama_stadium, pk.jenis_partai, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, s.kapasitas
        ORDER BY e.tgl_mulai;
        '''
    )]
    print(event)
    return render (request, 'listEvent.html', {'data':event})

# def lihat_event(request):
#     event = {}
#     event['event'] = [event._asdict() for event in query(
#         f'''SELECT partai_kompetisi.nama_event, tahun, nama_stadium, jenis_partai, kategori_superseries, tgl_mulai, tgl_selesai, kapasitas FROM partai_kompetisi
#         JOIN event e on partai_kompetisi.nama_event = e.nama_event and partai_kompetisi.tahun_event = e.tahun
#         JOIN stadium s on e.nama_stadium = s.nama;
#         '''
#     )]
#     return render (request, 'listEvent.html', {'data':event})

# def lihat_event(request):
#     temp = {}
#     temp = [event._asdict() for event in query(
#         f'''SELECT * FROM
#         '''
#     )]
#     event = {}
#     event['event'] = [event._asdict() for event in query(
#         f'''SELECT partai_kompetisi.nama_event, tahun, nama_stadium, jenis_partai, kategori_superseries, tgl_mulai, tgl_selesai, kapasitas FROM partai_kompetisi
#         JOIN event e on partai_kompetisi.nama_event = e.nama_event and partai_kompetisi.tahun_event = e.tahun
#         JOIN stadium s on e.nama_stadium = s.nama;
#         '''
#     )]
#     return render (request, 'listEvent.html', {'data':event})

def pertandingan(request, prtdg):
    return render (request, 'pertandingan.html')

def hasil_pertandingan(request, nama_event, tahun):
    detail = {}

    detail['detail'] = [detail._asdict() for detail in query(
        f'''SELECT nama_event, total_hadiah, tgl_mulai, tgl_selesai, 
            kategori_superseries, kapasitas, nama_stadium FROM event
            JOIN stadium s on s.nama = event.nama_stadium
            WHERE nama_event = '{nama_event}' AND tahun = {tahun};
        '''
    )]
    # print(detail)
    hasil_pertandingan = {}
    # hasil_pertandingan['hasil_pertandingan'] = [hasil_pertandingan._asdict() for hasil_pertandingan in query(
    #     f'''SELECT ;
    #     '''
    # )]
    # return render (request, 'hasilPertandingan.html', {'hasil_pertandingan': hasil_pertandingan})
    return render (request, 'hasilPertandingan.html', {'detail':detail})

