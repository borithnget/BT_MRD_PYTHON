# Generated by Django 4.1.1 on 2022-10-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0007_watersupplytype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watersupplytype',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
