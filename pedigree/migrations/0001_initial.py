# Generated by Django 2.1.2 on 2018-10-13 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breeder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(blank=True, max_length=100)),
                ('contact_name', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=250)),
                ('phone_number1', models.CharField(blank=True, max_length=100)),
                ('phone_number2', models.CharField(blank=True, max_length=100)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Goat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_no', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('date_of_registration', models.DateField(blank=True)),
                ('dob', models.CharField(blank=True, max_length=100)),
                ('dod', models.CharField(blank=True, max_length=100)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')], default='Unknown', max_length=10)),
                ('sire', models.CharField(blank=True, max_length=100)),
                ('dam', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('min_milk_yield', models.CharField(blank=True, max_length=100)),
                ('max_milk_yield', models.CharField(blank=True, max_length=100)),
                ('avg_milk_yield', models.CharField(blank=True, max_length=100)),
                ('height_to_withers', models.CharField(blank=True, max_length=100)),
                ('first_prize', models.BooleanField(default=False)),
                ('second_prize', models.BooleanField(default=False)),
                ('third_prize', models.BooleanField(default=False)),
                ('breeder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pedigree.Breeder')),
                ('current_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pedigree.Breeder')),
            ],
        ),
    ]
