# Generated by Django 2.1.7 on 2019-04-01 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tips', '0002_auto_20190329_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipper',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tip',
            name='tipper',
        ),
        migrations.AddField(
            model_name='tip',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='snippets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Tipper',
        ),
    ]
