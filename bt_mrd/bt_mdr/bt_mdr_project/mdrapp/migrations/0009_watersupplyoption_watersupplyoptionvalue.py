# Generated by Django 4.1.1 on 2022-10-10 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0008_alter_watersupplytype_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterSupplyOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('name_en', models.TextField(blank=True, default='', null=True)),
                ('name_kh', models.TextField(blank=True, default='', null=True)),
                ('data_type', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaterSupplyOptionValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('name_en', models.TextField(blank=True, default='', null=True)),
                ('name_kh', models.TextField(blank=True, default='', null=True)),
                ('description', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('water_supply_option_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdrapp.watersupplyoption')),
            ],
        ),
    ]
