# Generated by Django 3.2.9 on 2021-12-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0010_auto_20211205_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='goals',
            field=models.ManyToManyField(blank=True, null=True, related_name='volunteer_profile', to='volunteer.Goal', verbose_name='Maqsad'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='languages',
            field=models.ManyToManyField(blank=True, null=True, related_name='volunteer_profile', to='volunteer.Language', verbose_name='Til'),
        ),
    ]
