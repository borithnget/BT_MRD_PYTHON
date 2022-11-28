# Generated by Django 4.1.1 on 2022-10-10 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0004_alter_district_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='code_en',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='district',
            name='code_kh',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='province',
            name='code_en',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='province',
            name='code_kh',
            field=models.CharField(default='', max_length=255),
        ),
    ]
