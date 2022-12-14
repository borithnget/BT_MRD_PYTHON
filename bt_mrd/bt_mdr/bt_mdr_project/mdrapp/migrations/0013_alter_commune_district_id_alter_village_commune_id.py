# Generated by Django 4.1.1 on 2022-10-13 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0012_alter_district_province_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='district_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districtcommnue', to='mdrapp.district'),
        ),
        migrations.AlterField(
            model_name='village',
            name='commune_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commnuevillage', to='mdrapp.commune'),
        ),
    ]
