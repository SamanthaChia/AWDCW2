# Generated by Django 2.2.15 on 2022-03-03 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='hide_phone',
        ),
        migrations.RemoveField(
            model_name='account',
            name='phone',
        ),
    ]
