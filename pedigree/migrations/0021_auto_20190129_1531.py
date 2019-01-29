# Generated by Django 2.1.2 on 2019-01-29 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedigree', '0020_auto_20190129_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedigree',
            name='breeder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='breeder.Breeder'),
        ),
        migrations.AlterField(
            model_name='pedigree',
            name='current_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='breeder.Breeder'),
        ),
        migrations.DeleteModel(
            name='Breeder',
        ),
    ]
