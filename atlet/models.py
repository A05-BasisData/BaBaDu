from django.db import models

class sponsor(models.Model):
    nama_sponsor = models.CharField(max_length=50)
    tgl_mulai = models.DateField()
    tgl_selesai = models.DateField()

