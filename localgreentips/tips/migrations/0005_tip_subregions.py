# Generated by Django 2.1.7 on 2019-11-13 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0011_auto_20180108_0706'),
        ('tips', '0004_auto_20190401_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='tip',
            name='subregions',
            field=models.ManyToManyField(blank=True, to='cities.Subregion'),
        ),
    ]
