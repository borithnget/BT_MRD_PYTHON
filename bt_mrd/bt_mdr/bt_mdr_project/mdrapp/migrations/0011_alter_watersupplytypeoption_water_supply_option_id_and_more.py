# Generated by Django 4.1.1 on 2022-10-12 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0010_watersupplytypeoption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watersupplytypeoption',
            name='water_supply_option_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watersupplytypeoption_option', to='mdrapp.watersupplyoption'),
        ),
        migrations.AlterField(
            model_name='watersupplytypeoption',
            name='water_supply_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watersupplytypeoption_type', to='mdrapp.watersupplytype'),
        ),
    ]
