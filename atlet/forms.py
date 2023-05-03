from django import forms
from django.forms import ModelForm
from atlet.models import *

SPONSOR_CHOICES = [('Gudang Garam', 'Gudang Garam'), ('Djarum', 'Djarum')]

class regist_sponsor(ModelForm):
    class Meta:
        model = sponsor
        fields = ('nama_sponsor', 'tgl_mulai', 'tgl_selesai')

    nama_sponsor = forms.CharField(label='Nama Sponsor', widget=forms.Select(choices=SPONSOR_CHOICES, attrs={'class': 'font-p'}))
    tgl_mulai = forms.DateField(label="Tanggal Mulai", widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control text-center font-p text-muted'}))
    tgl_selesai = forms.DateField(label="Tanggal Selesai", widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control text-center font-p text-muted'}))