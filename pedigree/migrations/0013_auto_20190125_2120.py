# Generated by Django 2.1.2 on 2019-01-25 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedigree', '0012_auto_20190125_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedigreeattributes',
            name='id',
        ),
        migrations.AlterField(
            model_name='pedigreeattributes',
            name='reg_no',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pedigree.Pedigree'),
        ),
    ]
