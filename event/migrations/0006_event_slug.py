# Generated by Django 3.2 on 2021-12-07 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_alter_volunteerforevent_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
