# Generated by Django 3.2.16 on 2022-11-29 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0020_watersupplyvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='watersupplyoption',
            name='field_name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
