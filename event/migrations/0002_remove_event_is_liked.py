# Generated by Django 3.2 on 2021-12-03 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_liked',
        ),
    ]
