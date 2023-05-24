from django.shortcuts import render
from utility.query import query

def dashboard_umpire(request):
    return render (request, 'dashboardUmpire.html')

def umpire_daftar_atlet(request):
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

    # print(atlet_non_kualifikasi)
    # print(atlet_ganda)
    # atlet_ganda['atlet_ganda'] = [atlet_ganda._asdict() for atlet_ganda in query(
    #     f'''SELECT ID_Atlet_Ganda, AK1.Nama, AK2.Nama, SUM(AK1.Total_Point, AK2.Total_Point)
    #     FROM ATLET_GANDA AG JOIN ATLET_KUALIFIKASI AK1, AK2 ON (AG.ID_Atlet_Kualifikasi = AK1.ID_ATLET OR AG.ID_Atlet_Kualifikasi_2 = AK2.ID_ATLET) 
    #     INNER JOIN (SELECT ID_Atlet, MAX(Total_Point) AS Total_Point FROM POINT_HISTORY GROUP BY ID_Atlet) PH ON A.ID = PH.ID_Atlet;
    #     '''
    # )]
    # print(atlet_ganda)

    context = {
        'data_ak':atlet_kualifikasi,
        'data_ank':atlet_non_kualifikasi,
        'data_ag':atlet_ganda
    }

    return render (request, 'umpireDaftarAtlet.html', context)

def lihat_event(request):
    event = {}
    event['event'] = [event._asdict() for event in query(
        f'''SELECT partai_kompetisi.nama_event, tahun, nama_stadium, jenis_partai, kategori_superseries, tgl_mulai, tgl_selesai, kapasitas FROM partai_kompetisi
        JOIN event e on partai_kompetisi.nama_event = e.nama_event and partai_kompetisi.tahun_event = e.tahun
        JOIN stadium s on e.nama_stadium = s.nama;
        '''
    )]
    return render (request, 'listEvent.html', {'data':event})

def pertandingan(request, prtdg):
    return render (request, 'pertandingan.html')

def hasil_pertandingan(request):
    # hasil_pertandingan = {}
    # hasil_pertandingan['hasil_pertandingan'] = [hasil_pertandingan._asdict() for hasil_pertandingan in query(
    #     f'''SELECT ;
    #     '''
    # )]
    # return render (request, 'hasilPertandingan.html', {'hasil_pertandingan': hasil_pertandingan})
    return render (request, 'hasilPertandingan.html')
