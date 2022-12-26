# Generated by Django 4.1.1 on 2022-11-30 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0023_watersupplywell_well_nirodynamic'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterSupplyRainWaterHarvesting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('type_of_using', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('capacity_35m3', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('capacity_4m3', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('capacity_of_rain_water_harvesting', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('status', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('status_no_reason', models.TextField(blank=True, default='', null=True)),
                ('watersupply_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watersupplyRainWaterHarvesting_watersupply', to='mdrapp.watersupply')),
            ],
        ),
        migrations.CreateModel(
            name='WaterSupplyPipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('source_type_of_water', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('abilty_of_produce_water', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('underground_pool_storage', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('pool_air', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('pool_filter', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('number_of_link', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('water_quality_check', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('status', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('status_no_reason', models.TextField(blank=True, default='', null=True)),
                ('watersupply_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watersupplypipe_watersupply', to='mdrapp.watersupply')),
            ],
        ),
        migrations.CreateModel(
            name='WaterSupplyKiosk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('source_type_of_water', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('abilty_of_produce_water', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('filter_system', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('status', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('status_no_reason', models.TextField(blank=True, default='', null=True)),
                ('watersupply_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watersupplyKiosk_watersupply', to='mdrapp.watersupply')),
            ],
        ),
        migrations.CreateModel(
            name='WaterSupplyCommunityPond',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('width', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('length', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('height', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('pool_filter', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('type_of_pond', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('is_summer_has_water', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('status', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('status_no_reason', models.TextField(blank=True, default='', null=True)),
                ('watersupply_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watersupplyCommunityPond_watersupply', to='mdrapp.watersupply')),
            ],
        ),
    ]