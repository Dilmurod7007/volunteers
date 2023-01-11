# Generated by Django 3.2 on 2021-12-07 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_volunteerforevent_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteerforevent',
            name='status',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Active'), (2, 'Finished')], default=1, null=True, verbose_name='Xolati'),
        ),
    ]
