# Generated by Django 4.1.6 on 2023-04-11 20:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simapp', '0033_delete_subsys_menu_remove_subsystem_command_buffer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='final_pitch',
            field=models.IntegerField(blank=True, default=-66, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)]),
        ),
        migrations.AlterField(
            model_name='mission',
            name='final_roll',
            field=models.IntegerField(blank=True, default=-87, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
        ),
        migrations.AlterField(
            model_name='mission',
            name='final_yaw',
            field=models.IntegerField(blank=True, default=-112, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
        ),
    ]
