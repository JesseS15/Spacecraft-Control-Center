# Generated by Django 4.1.2 on 2023-03-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ACS_Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BufferItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buffer_item', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Sim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sim_name', models.CharField(default='', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Subsys_Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Subsystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sys_name', models.CharField(default='', max_length=15)),
                ('button_value', models.BooleanField(default=True)),
            ],
        ),
    ]
