# Generated by Django 2.1.7 on 2019-03-29 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tip',
            old_name='user',
            new_name='tipper',
        ),
    ]