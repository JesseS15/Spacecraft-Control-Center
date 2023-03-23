# Generated by Django 4.1.2 on 2023-03-23 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fo', '0009_flightoperator_class_list'),
        ('simapp', '0030_remove_sim_flight_director'),
    ]

    operations = [
        migrations.AddField(
            model_name='sim',
            name='flight_director',
            field=models.ManyToManyField(blank=True, default='', related_name='flight_director', to='fo.flightoperator', verbose_name='Flight Director'),
        ),
    ]
