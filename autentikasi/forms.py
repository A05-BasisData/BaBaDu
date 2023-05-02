from django import forms
from django.forms import ModelForm
from autentikasi.models import *

class regist_form_atlet(ModelForm):
    class Meta:
        model = Atlet
        fields = ('nama',
                  'email',
                  'negara_asal', 
                  'tgl_lahir', 
                  'play_right',
                  'height',
                  'jenis_kelamin')
    
    nama = forms.CharField(label="Nama", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class': 'form-control text-center font-p', 'placeholder': 'Ex: LoremIpsum@gmail.com'}), max_length=50)
    negara_asal = forms.CharField(label="Negara", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # tgl_lahir = forms.DateField(label="Tanggal Lahir", widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control text-center font-p text-muted'})) #harusnya charfield
    tgl_lahir = forms.CharField(label="Tanggal Lahir", widget=forms.TextInput(attrs={'class': 'form-control'}))
    play_right = forms.TypedChoiceField(
                   coerce=lambda x: x == 'True',
                   choices=((False, 'Left'), (True, 'Right')),
                   widget=forms.RadioSelect(attrs={'class': 'font-p'}),
                   label="Play"
                )
    height = forms.IntegerField(label="Tinggi Badan", widget=forms.TextInput(attrs={'class': 'form-control'}))
    jenis_kelamin = forms.TypedChoiceField(
                   coerce=lambda x: x == 'True',
                   choices=((False, 'Putri'), (True, 'Putra')),
                   widget=forms.RadioSelect(attrs={'class': 'font-p'}),
                   label="Jenis Kelamin"
                )

class regist_form_pelatih(ModelForm):
    class Meta:
        model = Atlet
        fields = ('nama',
                  'email',
                  'negara_asal',
                  'kategori',
                  'tgl_mulai')
    
    nama = forms.CharField(label="Nama", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class': 'form-control text-center font-p', 'placeholder': 'Ex: LoremIpsum@gmail.com'}), max_length=50)
    negara_asal = forms.CharField(label="Negara", widget=forms.TextInput(attrs={'class': 'form-control'}))
    tgl_mulai = forms.DateField(label="Tanggal Mulai", widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control text-center font-p text-muted'}))
    kategori = forms.MultipleChoiceField(widget= forms.CheckboxSelectMultiple(attrs={'class': 'font-p'}),
            choices = 
             (('Tunggal Putra', 'Tunggal Putra'),
              ('Tunggal Putri', 'Tunggal Putri'),
              ('Ganda Putra', 'Ganda Putra'),
              ('Ganda Putri', 'Ganda Putri'),
              ('Ganda Campuran', 'Ganda Campuran')),
            label="Kategori"
            )

class regist_form_umpire(ModelForm):
    class Meta:
        model = Atlet
        fields = ('nama',
                  'email',
                  'negara_asal',)
    
    nama = forms.CharField(label="Nama", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class': 'form-control text-center font-p', 'placeholder': 'Ex: LoremIpsum@gmail.com'}), max_length=50)
    negara_asal = forms.CharField(label="Negara", widget=forms.TextInput(attrs={'class': 'form-control'}))
