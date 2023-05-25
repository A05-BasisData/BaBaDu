from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from atlet.forms import *
from autentikasi.views import *
from utility.query import query
import uuid

def dashboard_atlet(request):
    if not is_authenticated(request):
        return redirect('/login')
    
    if request.session["role"] != "atlet":
        return HttpResponse("401 Unauthorized: Unauthorized session role Atlet")
    
    atlet_data = query(
        f'''SELECT m.nama, negara_asal, m.email, tgl_lahir, play_right, height, jenis_kelamin FROM atlet
            JOIN member m on m.id = atlet.id
            WHERE m.nama = '{request.session["nama"]}' AND m.email = '{request.session["email"]}';
        '''
    )

    nama_lengkap = atlet_data[0].nama
    negara = atlet_data[0].negara_asal
    email = atlet_data[0].email
    tanggal_lahir = atlet_data[0].tgl_lahir
    play_right = atlet_data[0].play_right
    if play_right == True: play_right = 'Right Hand'
    else: play_right = 'Left Hand'

    tinggi_badan = atlet_data[0].height
    jenis_kelamin = atlet_data[0].jenis_kelamin
    if jenis_kelamin == True: jenis_kelamin = 'Putri'
    else: jenis_kelamin = 'Putra'

    pelatih = ''
    pelatih_temp = query(
        f'''SELECT nama FROM member
            JOIN pelatih p on member.id = p.id
            JOIN atlet_pelatih ap on p.id = ap.id_pelatih
            WHERE ap.id_atlet = '{request.session["id"]}'
        '''
    )
    if len(pelatih_temp) == 0: pelatih = "-"
    else: pelatih = pelatih_temp[0].nama

    status = ''
    world_rank = '-'
    total_point = 0 
    atlet_kualifikasi_temp = query(
        f'''SELECT * FROM atlet_kualifikasi
            WHERE id_atlet = '{request.session["id"]}'
        '''
    )
    if len(atlet_kualifikasi_temp) == 0: 
        status = "Not Qualified"
    else:
        temp_point = query(
            f'''SELECT sum(total_point) AS sum_point FROM point_history
                WHERE id_atlet = '{request.session["id"]}'
                GROUP BY  id_atlet;
            '''
        )
        status = "Qualified"
        world_rank = atlet_kualifikasi_temp[0].world_rank
        total_point = temp_point[0].sum_point

    context = {
        "Nama_Lengkap" : nama_lengkap,
        "Negara" : negara,
        "Email" : email,
        "Tanggal_Lahir" : tanggal_lahir,
        "Play" : play_right,
        "Tinggi_Badan" : tinggi_badan,
        "Jenis_Kelamin" : jenis_kelamin,
        "Pelatih" : pelatih,
        "Status" : status,
        "World_Rank" : world_rank,
        "Total_Poin" : total_point
    }
    return render (request, 'dashboardAtlet.html', context)

def tes_kualifikasi(request):
    return render (request, 'tesKualifikasi.html')

def pertanyaan_kualifikasi(request):
    return render (request, 'pertanyaanKualifikasi.html')

def pilih_stadium(request):
    if not is_authenticated(request):
        return redirect('/login')
    
    if request.session["role"] != "atlet":
        return HttpResponse("401 Unauthorized: Unauthorized session role Pelanggan")

    data = {}
    data['stadium'] = [std._asdict() for std in query(
        f'''SELECT * FROM STADIUM
            ORDER BY kapasitas;'''
    )]

    # print("=====================")
    # print("Stadium detail")
    # print(data['stadium'])
    # print("=====================")

    return render (request, 'pilihStadium.html', {'data':data})

def daftar_event(request, evname, evthn):

    if not is_authenticated(request):
        return redirect('/login')
    
    if request.session["role"] != "atlet":
        return HttpResponse("401 Unauthorized: Unauthorized session role Pelanggan")
    
    data = {}
    detail = {}
    temp_partai = {}

    detail = query(
        f'''SELECT nama_event, total_hadiah, tgl_mulai, tgl_selesai, 
            kategori_superseries, kapasitas, nama_stadium, event.negara FROM event
            JOIN stadium s on s.nama = event.nama_stadium
            WHERE nama_event = '{evname}' AND tahun = {evthn};
        '''
    )
    
    partai_count = query(
        f'''SELECT COUNT(*) FROM partai_kompetisi
            WHERE nama_event = '{evname}' AND tahun_event = {evthn};
        '''
    )
    temp_partai = query(
        f'''SELECT jenis_partai FROM partai_kompetisi
            WHERE nama_event = '{evname}' AND tahun_event = {evthn}
            ORDER BY jenis_partai DESC;
        '''
    )

    # Contoh
    jenis_kelamin = query(
        f'''SELECT jenis_kelamin FROM ATLET
        WHERE id = '{request.session["id"]}'
        '''
    )

    # for i in len(partai_pendaftar):
    #     if (partai_pendaftar[i].jenis_partai)[:5] == 'Ganda':
    #         kapasitas_terisi = kapasitas_terisi +2
    #     else:
    #         kapasitas_terisi = kapasitas_terisi +1
    partai_pendaftar = query(
        f'''SELECT jenis_partai FROM peserta_mendaftar_event
            JOIN partai_peserta_kompetisi ppk on peserta_mendaftar_event.nomor_peserta = ppk.nomor_peserta
            WHERE peserta_mendaftar_event.nama_event = '{evname}' AND peserta_mendaftar_event.tahun = {evthn} AND ppk.nama_event = '{evname}' '''
    )

    pertandingan = []
    for i in range (partai_count[0].count):
        jns_partai = temp_partai[i].jenis_partai

        if jenis_kelamin[0].jenis_kelamin == True:
            if jns_partai == 'WS':
                kapasitas_terisi = 0
                for k in range (len(partai_pendaftar)):
                    if partai_pendaftar[k].jenis_partai == 'WS':
                        kapasitas_terisi = kapasitas_terisi + 1
                temp = {'Partai' : 'Tunggal Putri', 'Partner' : '-', 'Kapasitas' : detail[0].kapasitas, 'Kapasitas_x' : kapasitas_terisi}
                pertandingan.append(temp)
            if jns_partai == 'WD':
                kapasitas_terisi = 0
                for k in range (len(partai_pendaftar)):
                    if partai_pendaftar[k].jenis_partai == 'WD':
                        kapasitas_terisi = kapasitas_terisi + 2
                get_partner = query(
                    f'''SELECT nama FROM member
                        JOIN atlet a on member.id = a.id
                        JOIN atlet_kualifikasi ak on a.id = ak.id_atlet
                        WHERE member.id NOT IN (
                            SELECT atlet_ganda.id_atlet_kualifikasi from atlet_ganda
                            JOIN atlet_kualifikasi k on atlet_ganda.id_atlet_kualifikasi = k.id_atlet
                            JOIN peserta_kompetisi pk on atlet_ganda.id_atlet_ganda = pk.id_atlet_ganda
                            JOIN partai_peserta_kompetisi ppk on pk.nomor_peserta = ppk.nomor_peserta
                            WHERE ppk.nama_event = '{evname}' AND ppk.tahun_event = '{evthn}' AND atlet_ganda.id_atlet_kualifikasi_2 = '{request.session["id"]}'
                            UNION 
                            SELECT atlet_ganda.id_atlet_kualifikasi_2 from atlet_ganda
                            JOIN atlet_kualifikasi k on atlet_ganda.id_atlet_kualifikasi = k.id_atlet
                            JOIN peserta_kompetisi pk on atlet_ganda.id_atlet_ganda = pk.id_atlet_ganda
                            JOIN partai_peserta_kompetisi ppk on pk.nomor_peserta = ppk.nomor_peserta
                            WHERE ppk.nama_event = '{evname}' AND ppk.tahun_event = '{evthn}' AND atlet_ganda.id_atlet_kualifikasi = '{request.session["id"]}'
                            )
                        AND jenis_kelamin = TRUE;
                    '''
                )
                partner_list = []
                if (len(get_partner)) != 0:
                    for j in range (len(get_partner)):
                        partner_list.append(get_partner[j].nama)

                temp = {'Partai' : 'Ganda Putri', 'Partner' : partner_list, 'Kapasitas' : detail[0].kapasitas, 'Kapasitas_x' : kapasitas_terisi}
                pertandingan.append(temp)
            if jns_partai == 'CD':
                # IF CASE FOR M AND W
                kapasitas_terisi = 0
                for k in range (len(partai_pendaftar)):
                    if partai_pendaftar[k].jenis_partai == 'CD':
                        kapasitas_terisi = kapasitas_terisi + 2
                get_partner = query(
                    f'''SELECT nama FROM member
                        JOIN atlet a on member.id = a.id
                        JOIN atlet_kualifikasi ak on a.id = ak.id_atlet
                        WHERE member.id NOT IN (
                            SELECT atlet_ganda.id_atlet_kualifikasi from atlet_ganda
                            JOIN atlet_kualifikasi k on atlet_ganda.id_atlet_kualifikasi = k.id_atlet
                            JOIN peserta_kompetisi pk on atlet_ganda.id_atlet_ganda = pk.id_atlet_ganda
                            JOIN partai_peserta_kompetisi ppk on pk.nomor_peserta = ppk.nomor_peserta
                            WHERE ppk.nama_event = '{evname}' AND ppk.tahun_event = '{evthn}' AND atlet_ganda.id_atlet_kualifikasi_2 = '{request.session["id"]}'
                            UNION 
                            SELECT atlet_ganda.id_atlet_kualifikasi_2 from atlet_ganda
                            JOIN atlet_kualifikasi k on atlet_ganda.id_atlet_kualifikasi = k.id_atlet
                            JOIN peserta_kompetisi pk on atlet_ganda.id_atlet_ganda = pk.id_atlet_ganda
                            JOIN partai_peserta_kompetisi ppk on pk.nomor_peserta = ppk.nomor_peserta
                            WHERE ppk.nama_event = '{evname}' AND ppk.tahun_event = '{evthn}' AND atlet_ganda.id_atlet_kualifikasi = '{request.session["id"]}'
                            )
                        AND jenis_kelamin = FALSE;
                    '''
                )
                partner_list = []
                if (len(get_partner)) != 0:
                    for j in range (len(get_partner)):
                        partner_list.append(get_partner[j].nama)

                temp = {'Partai' : 'Ganda Campuran', 'Partner' : partner_list,'Kapasitas' : detail[0].kapasitas, 'Kapasitas_x' : kapasitas_terisi}
                pertandingan.append(temp)

        else:
            if jns_partai == 'MS':
                kapasitas_terisi = 0
                for k in range (len(partai_pendaftar)):
                    if partai_pendaftar[k].jenis_partai == 'MS':
                        kapasitas_terisi = kapasitas_terisi + 1
                temp = {'Partai' : 'Tunggal Putra', 'Partner' : '-', 'Kapasitas' : detail[0].kapasitas, 'Kapasitas_x' : kapasitas_terisi}
                pertandingan.append(temp)
            if jns_partai == 'MD':
                kapasitas_terisi = 0
                for k in range (len(partai_pendaftar)):
                    if partai_pendaftar[k].jenis_partai == 'MD':
                        kapasitas_terisi = kapasitas_terisi + 2
                get_partner = query(
                    f'''SELECT nama FROM member
                        JOIN atlet a on member.id = a.id
                        JOIN atlet_kualifikasi ak on a.id = ak.id_atlet
                        WHERE member.id NOT IN (
                            SELECT atlet_ganda.id_atlet_kualifikasi from atlet_ganda
                            JOIN atlet_kualifikasi k on atlet_ganda.id_atlet_kualifikasi = k.id_atlet
                            JOIN peserta_kompetisi pk on atlet_ganda.id_atlet_ganda = pk.id_atlet_ganda
                            JOIN partai_peserta_kompetisi ppk on pk.nomor_peserta = ppk.nomor_peserta
                            WHERE ppk.nama_event = '{evname}' AND ppk.tahun_event = '{evthn}' AND atlet_ganda.id_atlet_kualifikasi_2 = '{request.session["id"]}'
                            UNION 
                            SELECT atlet_ganda.id_atlet_kualifikasi_2 from atlet_ganda
                            JOIN atlet_kualifikasi k on atlet_ganda.id_atlet_kualifikasi = k.id_atlet
                            JOIN peserta_kompetisi pk on atlet_ganda.id_atlet_ganda = pk.id_atlet_ganda
                            JOIN partai_peserta_kompetisi ppk on pk.nomor_peserta = ppk.nomor_peserta 
                            WHERE ppk.nama_event = '{evname}' AND ppk.tahun_event = '{evthn}'AND atlet_ganda.id_atlet_kualifikasi = '{request.session["id"]}'
                            )
                        AND jenis_kelamin = FALSE;
                    '''
                )
                partner_list = []
                if (len(get_partner)) != 0:
                    for j in range (len(get_partner)):
                        partner_list.append(get_partner[j].nama)

                temp = {'Partai' : 'Ganda Putra', 'Partner' : partner_list, 'Kapasitas' : detail[0].kapasitas, 'Kapasitas_x' : kapasitas_terisi}
                pertandingan.append(temp)
            if jns_partai == 'CD':
                kapasitas_terisi = 0
                for k in range (len(partai_pendaftar)):
                    if partai_pendaftar[k].jenis_partai == 'CD':
                        kapasitas_terisi = kapasitas_terisi + 2
                get_partner = query(
                    f'''SELECT nama FROM member
                        JOIN atlet a on member.id = a.id
                        JOIN atlet_kualifikasi ak on a.id = ak.id_atlet
                        WHERE member.id NOT IN (
                            SELECT atlet_ganda.id_atlet_kualifikasi from atlet_ganda
                            JOIN atlet_kualifikasi k on atlet_ganda.id_atlet_kualifikasi = k.id_atlet
                            JOIN peserta_kompetisi pk on atlet_ganda.id_atlet_ganda = pk.id_atlet_ganda
                            JOIN partai_peserta_kompetisi ppk on pk.nomor_peserta = ppk.nomor_peserta
                            WHERE ppk.nama_event = '{evname}' AND ppk.tahun_event = '{evthn}' AND atlet_ganda.id_atlet_kualifikasi_2 = '{request.session["id"]}'
                            UNION 
                            SELECT atlet_ganda.id_atlet_kualifikasi_2 from atlet_ganda
                            JOIN atlet_kualifikasi k on atlet_ganda.id_atlet_kualifikasi = k.id_atlet
                            JOIN peserta_kompetisi pk on atlet_ganda.id_atlet_ganda = pk.id_atlet_ganda
                            JOIN partai_peserta_kompetisi ppk on pk.nomor_peserta = ppk.nomor_peserta
                            WHERE ppk.nama_event = '{evname}' AND ppk.tahun_event = '{evthn}' AND atlet_ganda.id_atlet_kualifikasi = '{request.session["id"]}'
                            )
                        AND jenis_kelamin = TRUE;
                    '''
                )
                partner_list = []
                if (len(get_partner)) != 0:
                    for j in range (len(get_partner)):
                        partner_list.append(get_partner[j].nama)

                temp = {'Partai' : 'Ganda Campuran', 'Partner' : partner_list, 'Kapasitas' : detail[0].kapasitas, 'Kapasitas_x' : kapasitas_terisi}
                pertandingan.append(temp)

    data['detail'] = detail[0]
    data['pertandingan'] = pertandingan
    data['kapasitas_2'] = ''

    print(pertandingan)

    if request.method == 'POST':
        jenis_partai = request.POST.get('jenis_partai')
        slc_partner = request.POST.get('slc_partner')

        print(jenis_partai)
        print(slc_partner)

        partner_id = query(
            f'''SELECT member.id FROM member
            WHERE member.nama = '{slc_partner}'
            '''
        )

        curr_no_psrt =''
        get_no_psrt = (query(f'''SELECT nomor_peserta FROM peserta_kompetisi
                                ORDER BY nomor_peserta DESC LIMIT 1'''))

        if jenis_partai[:5] == 'Ganda':
            # Kurang ID user, masih dummy
            curr_id_psrt = uuid.uuid1()
            avail_ganda_check = query(
                f'''SELECT id_atlet_kualifikasi, id_atlet_kualifikasi_2 FROM atlet_ganda
                    WHERE (id_atlet_kualifikasi = '{request.session["id"]}' AND id_atlet_kualifikasi_2 = '{partner_id[0].id}')
                    OR (id_atlet_kualifikasi = '{partner_id[0].id}' AND id_atlet_kualifikasi_2 = '{request.session["id"]}')
                '''
                )
            if len(avail_ganda_check) == 0:
                print(query(
                    f'''INSERT INTO atlet_ganda 
                    VALUES('{curr_id_psrt}', '{request.session["id"]}', '{partner_id[0].id}')
                    '''
                ))

            avail_daftar_ganda_check = query(
                f'''SELECT nomor_peserta FROM peserta_kompetisi
                    JOIN atlet_ganda ag on peserta_kompetisi.id_atlet_ganda = ag.id_atlet_ganda
                    WHERE (ag.id_atlet_kualifikasi = '{request.session["id"]}' AND ag.id_atlet_kualifikasi_2 = '{partner_id[0].id}')
                    OR (ag.id_atlet_kualifikasi = '{partner_id[0].id}' AND ag.id_atlet_kualifikasi_2 = '{request.session["id"]}')
                '''
                )

            if len(avail_daftar_ganda_check) == 0:
                get_wrld_rnk = (query(f'''SELECT world_rank, world_tour_rank FROM atlet_kualifikasi 
                                         WHERE id_atlet = '{request.session["id"]}' '''))
                curr_no_psrt = get_no_psrt[0].nomor_peserta + 2
                curr_wrld_rnk = get_wrld_rnk[0].world_rank
                curr_wrld_tr_rnk = get_wrld_rnk[0].world_tour_rank
                print(query(
                    f'''INSERT INTO peserta_kompetisi (nomor_peserta, id_atlet_ganda, world_rank, world_tour_rank)
                        VALUES ({curr_no_psrt}, '{curr_id_psrt}', {curr_wrld_rnk}, {curr_wrld_tr_rnk})
                    '''
                ))
            else:
                curr_no_psrt = avail_daftar_ganda_check[0].nomor_peserta
        else:
            avail_daftar_check = query(
                f'''SELECT id_atlet_kualifikasi FROM peserta_kompetisi
                    WHERE id_atlet_kualifikasi = '{request.session["id"]}';
                '''
            )
            if len(avail_daftar_check) == 0:
                get_wrld_rnk = (query(f'''SELECT world_rank, world_tour_rank FROM atlet_kualifikasi 
                                        WHERE id_atlet = '{request.session["id"]}' '''))
                curr_no_psrt = get_no_psrt[0].nomor_peserta + 2
                curr_wrld_rnk = get_wrld_rnk[0].world_rank
                curr_wrld_tr_rnk = get_wrld_rnk[0].world_tour_rank
                print(query(
                    f'''INSERT INTO peserta_kompetisi (nomor_peserta, id_atlet_kualifikasi, world_rank, world_tour_rank)
                        VALUES ({curr_no_psrt}, '{request.session["id"]}', {curr_wrld_rnk}, {curr_wrld_tr_rnk})
                    '''
                ))
            else:
                temp_1 = query(
                    f'''SELECT nomor_peserta FROM peserta_kompetisi
                        WHERE id_atlet_kualifikasi = '{request.session["id"]}';
                    '''
                )
                curr_no_psrt = temp_1[0].nomor_peserta
        
        jns_prti = ''
        if jenis_partai == 'Tunggal Putra': jns_prti = 'MS'
        if jenis_partai == 'Tunggal Putri': jns_prti = 'WS'
        if jenis_partai == 'Ganda Putra':  jns_prti = 'MD'
        if jenis_partai == 'Ganda Putri': jns_prti = 'WD'
        if jenis_partai == 'Ganda Campuran': jns_prti = 'CD'

        print(query(
            f'''INSERT INTO partai_peserta_kompetisi VALUES(
                '{jns_prti}', '{evname}', '{evthn}', '{curr_no_psrt}'
                )
            '''
        ))
        trigger_4 = (query(
            f'''INSERT INTO peserta_mendaftar_event VALUES(
                '{curr_no_psrt}', '{evname}', '{evthn}'
                )
            '''
        ))
        print(trigger_4)
        if isinstance(trigger_4, Exception):
            trigger_msg = trigger_4.args[0].split("\n")[0]
            messages.error(request, trigger_msg)
            return redirect("/atlet/daftar_event")
        return redirect("/atlet/enrolled_event")

    return render (request, 'daftarEventAtlet.html', {'data':data})

def pilih_event(request, stdname):
    if not is_authenticated(request):
        return redirect('/login')
    
    if request.session["role"] != "atlet":
        return HttpResponse("401 Unauthorized: Unauthorized session role Pelanggan")

    temp = {}
    cnt = query(
        f'''SELECT COUNT(*) FROM EVENT
            JOIN stadium s on s.nama = event.nama_stadium
            WHERE s.nama = '{stdname}'
        '''
    )
    temp = [event._asdict() for event in query(
        f'''SELECT nama_event, total_hadiah, tgl_mulai, kategori_superseries, tahun FROM EVENT
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


