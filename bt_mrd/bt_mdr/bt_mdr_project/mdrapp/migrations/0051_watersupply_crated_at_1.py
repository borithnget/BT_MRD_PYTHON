# Generated by Django 4.1.4 on 2023-03-15 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0050_alter_watersupplyairwateroptionvalue_water_supply_airwater_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='watersupply',
            name='crated_at_1',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
