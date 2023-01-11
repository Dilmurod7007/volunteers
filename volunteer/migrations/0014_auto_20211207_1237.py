# Generated by Django 3.2.9 on 2021-12-07 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0013_alter_volunteerrating_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='goals',
            field=models.ManyToManyField(blank=True, related_name='volunteer_profile', to='volunteer.Goal', verbose_name='Maqsad'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='volunteer_profile', to='volunteer.Language', verbose_name='Til'),
        ),
    ]
