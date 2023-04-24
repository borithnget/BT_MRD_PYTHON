# Generated by Django 4.1.4 on 2023-01-11 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0031_user_data_entry_province_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterSupplyQRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code_image_name', models.TextField(blank=True, default='', null=True)),
                ('watersupply_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watersupplyqrcode_watersupply', to='mdrapp.watersupply')),
            ],
        ),
    ]