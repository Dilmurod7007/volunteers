# Generated by Django 3.2 on 2021-12-07 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_event_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteerforevent',
            name='status',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Registered'), (2, 'Canceled')], default=1, null=True, verbose_name='Xolati'),
        ),
    ]
