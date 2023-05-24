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
    return render (request, 'listEvent.html', {'data':event})

def pertandingan(request, prtdg):
    return render (request, 'pertandingan.html')

def hasil_pertandingan(request):
    return render (request, 'hasilPertandingan.html')

def lihat_atlet(request):
    return render (request, 'listAtletUmpire.html')
