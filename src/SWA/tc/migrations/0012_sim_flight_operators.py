# Generated by Django 4.1.2 on 2022-12-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fo', '0004_flightoperator_sim_list'),
        ('tc', '0011_rename_simsys_subsystem'),
    ]

    operations = [
        migrations.AddField(
            model_name='sim',
            name='flight_operators',
            field=models.ManyToManyField(to='fo.flightoperator', verbose_name='Flight Operator'),
        ),
    ]
