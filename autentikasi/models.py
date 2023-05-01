import uuid
from django.db import models

# models for frontend purpose only
class Atlet(models.Model):
    id_member = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    nama = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    tgl_lahir = models.DateField()
    negara_asal = models.CharField(max_length=50)
    play_right = models.BooleanField()
    height = models.IntegerField()
    world_rank = models.IntegerField(default=999)
    jenis_kelamin = models.BooleanField()
    kualifikasi = models.BooleanField(default=False)

class Pelatih(models.Model):
    id_member = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    nama = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    negara_asal = models.CharField(max_length=50)
    kategori = models.TextField()
    tgl_mulai = models.DateField()

class Umpire(models.Model):
    id_member = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    nama = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    negara_asal = models.CharField(max_length=50)


