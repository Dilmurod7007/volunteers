# Generated by Django 3.2 on 2021-12-03 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_remove_event_is_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tag',
            name='word',
            field=models.CharField(max_length=50),
        ),
    ]