# Generated by Django 2.1.2 on 2018-10-15 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedigree', '0005_auto_20181015_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedigree',
            name='parent_father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farther', to='pedigree.Pedigree'),
        ),
        migrations.AlterField(
            model_name='pedigree',
            name='parent_mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mother', to='pedigree.Pedigree'),
        ),
    ]