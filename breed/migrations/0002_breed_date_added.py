# Generated by Django 2.1.2 on 2019-01-30 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='breed',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default='2019-01-30 22:00'),
            preserve_default=False,
        ),
    ]
