# Generated by Django 2.1.2 on 2019-02-01 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedigree', '0026_auto_20190131_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedigree',
            name='notes',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
