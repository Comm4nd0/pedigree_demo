# Generated by Django 2.1.2 on 2019-01-28 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedigree', '0018_auto_20190128_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='pedigree',
            name='breed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='breed', to='pedigree.Breed'),
        ),
    ]
