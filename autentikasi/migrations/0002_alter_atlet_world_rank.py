# Generated by Django 4.2 on 2023-05-03 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autentikasi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atlet',
            name='world_rank',
            field=models.IntegerField(default=999),
        ),
    ]