# Generated by Django 3.2 on 2021-12-06 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0003_auto_20211203_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteerforevent',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profilee', to='volunteer.user', verbose_name='Foydalanuvchi'),
            preserve_default=False,
        ),
    ]
