from django.shortcuts import render
from utility.query import query

def dashboard_umpire(request):
    return render (request, 'dashboardUmpire.html')

def lihat_event(request):
    event = {}
    event['event'] = [event._asdict() for event in query(
        f'''SELECT partai_kompetisi.nama_event, tahun, nama_stadium, jenis_partai, kategori_superseries, tgl_mulai, tgl_selesai, kapasitas FROM partai_kompetisi
        JOIN event e on partai_kompetisi.nama_event = e.nama_event and partai_kompetisi.tahun_event = e.tahun
        JOIN stadium s on e.nama_stadium = s.nama;
        '''
    )]
    
    for i in range (len(event['event'])):
        kapasitas_terisi = 0
        partai_pendaftar = query(
        f'''SELECT jenis_partai FROM peserta_mendaftar_event
            JOIN partai_peserta_kompetisi ppk on peserta_mendaftar_event.nomor_peserta = ppk.nomor_peserta
            WHERE peserta_mendaftar_event.nama_event = '{event['event'][i]['nama_event']}' AND peserta_mendaftar_event.tahun = {event['event'][i]['tahun']} AND ppk.nama_event = '{event['event'][i]['nama_event']}' '''
        )
        if event['event'][i]['jenis_partai'] == 'WS':
            for k in range (len(partai_pendaftar)):
                if partai_pendaftar[k].jenis_partai == 'WS':
                    kapasitas_terisi = kapasitas_terisi + 1
            event['event'][i]['kapasitas_pendaftar'] = kapasitas_terisi

        if event['event'][i]['jenis_partai'] == 'MS':
            for k in range (len(partai_pendaftar)):
                if partai_pendaftar[k].jenis_partai == 'MS':
                    kapasitas_terisi = kapasitas_terisi + 1
            event['event'][i]['kapasitas_pendaftar'] = kapasitas_terisi

        if event['event'][i]['jenis_partai'] == 'WD':
            for k in range (len(partai_pendaftar)):
                if partai_pendaftar[k].jenis_partai == 'WD':
                    kapasitas_terisi = kapasitas_terisi + 2
            event['event'][i]['kapasitas_pendaftar'] = kapasitas_terisi

        if event['event'][i]['jenis_partai'] == 'MD':
            for k in range (len(partai_pendaftar)):
                if partai_pendaftar[k].jenis_partai == 'MD':
                    kapasitas_terisi = kapasitas_terisi + 2
            event['event'][i]['kapasitas_pendaftar'] = kapasitas_terisi

        if event['event'][i]['jenis_partai'] == 'CD':
            for k in range (len(partai_pendaftar)):
                if partai_pendaftar[k].jenis_partai == 'CD':
                    kapasitas_terisi = kapasitas_terisi + 2
            event['event'][i]['kapasitas_pendaftar'] = kapasitas_terisi
        
    return render (request, 'listEvent.html', {'data':event})

def pertandingan(request, prtdg):
    return render (request, 'pertandingan.html')

def hasil_pertandingan(request):
    return render (request, 'hasilPertandingan.html')

def lihat_atlet(request):
    return render (request, 'listAtletUmpire.html')
