# Generated by Django 4.1.4 on 2023-02-22 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdrapp', '0048_watersupplypipeprivate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watersupplypipeprivate',
            name='is_has_license',
            field=models.CharField(blank=True, default='0', max_length=255, null=True),
        ),
    ]
