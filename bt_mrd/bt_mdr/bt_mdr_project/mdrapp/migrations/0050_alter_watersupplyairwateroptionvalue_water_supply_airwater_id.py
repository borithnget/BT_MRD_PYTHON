# Generated by Django 4.1.4 on 2023-02-22 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0049_alter_watersupplypipeprivate_is_has_license'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watersupplyairwateroptionvalue',
            name='water_supply_airwater_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watersupplyairwateroptionvalue_watersupplykioskwater', to='mdrapp.watersupplyairwater'),
        ),
    ]
