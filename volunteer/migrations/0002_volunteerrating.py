# Generated by Django 3.2.9 on 2021-12-03 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Kiritilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('rating', models.PositiveIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')], default=5, verbose_name='Reytinggi')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Tashkilot')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to=settings.AUTH_USER_MODEL, verbose_name='Volontyor')),
            ],
            options={
                'verbose_name': 'Volontyor reytinggi',
                'verbose_name_plural': 'Volontyorlar reytinggi',
            },
        ),
    ]
