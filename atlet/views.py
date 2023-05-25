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
    data = {}
    data['stadium'] = [std._asdict() for std in query(
        f'''SELECT * FROM STADIUM
            ORDER BY kapasitas;'''
    )]

    print("=====================")
    print("Stadium detail")
    print(data['stadium'])
    print("=====================")

    return render (request, 'pilihStadium.html', {'data':data})

def daftar_event(request, evname):
    data = {}
    detail = {}
    temp_partai = {}

    detail = query(
        f'''SELECT nama_event, total_hadiah, tgl_mulai, tgl_selesai, 
            kategori_superseries, kapasitas, nama_stadium, event.negara FROM event
            JOIN stadium s on s.nama = event.nama_stadium
            WHERE nama_event = '{evname}';
        '''
    )
    
    partai_count = query(
        f'''SELECT COUNT(*) FROM partai_kompetisi
            WHERE nama_event = '{evname}'
        '''
    )
    temp_partai = query(
        f'''SELECT jenis_partai FROM partai_kompetisi
            WHERE nama_event = '{evname}'
        '''
    )

    pertandingan = []
    # IF CASE FOR M AND W
    for i in range (partai_count[0].count):
        jns_partai = temp_partai[i].jenis_partai

        if jns_partai == 'MS':
            temp = {'Partai' : 'Tunggal Putra', 'Partner' : '-'}
            pertandingan.append(temp)
        if jns_partai == 'WS':
            temp = {'Partai' : 'Tunggal Putri', 'Partner' : '-'}
            pertandingan.append(temp)

        if jns_partai == 'MD':
            get_partner = query(
                f'''SELECT nama FROM member
                    JOIN atlet a on member.id = a.id
                    JOIN atlet_kualifikasi ak on a.id = ak.id_atlet
                    WHERE member.id NOT IN (
                        SELECT id_atlet_kualifikasi from atlet_ganda
                        UNION 
                        SELECT id_atlet_kualifikasi_2 from atlet_ganda
                        )
                    AND jenis_kelamin = FALSE;
                '''
            )
            partner_list = []
            for j in range (len(get_partner)):
                partner_list.append(get_partner[j].nama)

            temp = {'Partai' : 'Ganda Putra', 'Partner' : partner_list}
            pertandingan.append(temp)

        if jns_partai == 'WD':
            get_partner = query(
                f'''SELECT nama FROM member
                    JOIN atlet a on member.id = a.id
                    JOIN atlet_kualifikasi ak on a.id = ak.id_atlet
                    WHERE member.id NOT IN (
                        SELECT id_atlet_kualifikasi from atlet_ganda
                        UNION 
                        SELECT id_atlet_kualifikasi_2 from atlet_ganda
                        )
                    AND jenis_kelamin = TRUE;
                '''
            )
            partner_list = []
            for j in range (len(get_partner)):
                partner_list.append(get_partner[j].nama)

            temp = {'Partai' : 'Ganda Putri', 'Partner' : partner_list}
            pertandingan.append(temp)

        if jns_partai == 'CD':
            # IF CASE FOR M AND W
            temp = {'Partai' : 'Ganda Campuran', 'Partner' : '-'}
            pertandingan.append(temp)

    
    print("=====================")
    print('Event detail')
    print(detail[0])
    print("=====================")
    print('Partai detail')
    print(pertandingan)
    print("=====================")

    data['detail'] = detail[0]
    print(pertandingan)
    data['pertandingan'] = pertandingan

    return render (request, 'daftarEventAtlet.html', {'data':data})

def pilih_event(request, stdname):
    temp = {}
    cnt = query(
        f'''SELECT COUNT(*) FROM EVENT
            JOIN stadium s on s.nama = event.nama_stadium
            WHERE s.nama = '{stdname}'
        '''
    )
    temp = [event._asdict() for event in query(
        f'''SELECT nama_event, total_hadiah, tgl_mulai, kategori_superseries FROM EVENT
            JOIN stadium s on s.nama = event.nama_stadium
            WHERE s.nama = '{stdname}'
            ORDER BY nama_event;
        '''
    )]
    data = {}
    if len(temp) != 0:
        data = temp
        print("=====================")
        print('Event detail')
        print(data)
        print("=====================")
        return render (request, 'pilihEvent.html', {'data':data})
    else:
        return render (request, 'pilihEventEmpty.html')

def enrolled_event(request):
    if request.method == "POST":
        nomor_peserta = query(
            f'''SELECT nomor_peserta FROM peserta_kompetisi 
                WHERE id_atlet_kualifikasi = '{request.session["id"]}';
            '''
        )
        print(nomor_peserta[0].nomor_peserta)
        check_enroll = query(
            f'''DELETE FROM PESERTA_MENDAFTAR_EVENT 
                WHERE Nama_Event = '{request.POST["nama_event"]}' AND Nomor_Peserta = '{nomor_peserta[0].nomor_peserta}' AND Tahun = '{request.POST["tahun"]}';
            ''')
        print(check_enroll)
        if isinstance(check_enroll, Exception):
            trigger_msg = check_enroll.args[0].split("\n")[0]
            messages.error(request, trigger_msg) #{{trigger_msg}}
            return redirect("/atlet/enrolled_event") 
                
    temp = {}
    print(request.session["id"])
    query_get = query(
        f'''SELECT e.nama_event, e.tahun, e.nama_stadium, e.negara, e.tgl_mulai, e.tgl_selesai, e.kategori_superseries, e.total_hadiah 
            FROM event AS e, peserta_mendaftar_event AS pme, peserta_kompetisi AS pkp
            WHERE pkp.id_atlet_kualifikasi = '{request.session['id']}' AND pme.nomor_peserta = pkp.nomor_peserta AND
            e.nama_event = pme.nama_event AND e.tahun = pme.tahun;
        '''
    )
    print(query_get)
    temp = [event._asdict() for event in query_get]

    data = {}
    if len(temp) != 0:
        data = temp
        print("=====================")
        print(request.session["id"])
        print(data)
        print("=====================")
        return render (request, 'enrolledEvent.html', {'data':data})
    else:
        return render (request, 'pilihEventEmpty.html')
    
    

def enrolled_partai_event(request):
            
    return render (request, 'enrolledPartaiEvent.html')

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
        