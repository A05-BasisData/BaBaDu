# Generated by Django 4.2 on 2023-05-01 21:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atlet',
            fields=[
                ('id_member', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('tgl_lahir', models.DateField()),
                ('negara_asal', models.CharField(max_length=50)),
                ('play_right', models.BooleanField()),
                ('height', models.IntegerField()),
                ('world_rank', models.IntegerField()),
                ('jenis_kelamin', models.BooleanField()),
                ('kualifikasi', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Pelatih',
            fields=[
                ('id_member', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('negara_asal', models.CharField(max_length=50)),
                ('kategori', models.TextField()),
                ('tgl_mulai', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Umpire',
            fields=[
                ('id_member', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('negara_asal', models.CharField(max_length=50)),
            ],
        ),
    ]
