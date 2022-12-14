# Generated by Django 4.1.1 on 2022-10-10 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=500)),
                ('name_kh', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=500)),
                ('name_kh', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
                ('province_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdrapp.province')),
            ],
        ),
    ]
