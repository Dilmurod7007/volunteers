# Generated by Django 3.2.9 on 2021-12-04 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_rename_is_activa_menu_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Faolmi'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Faolmi'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='Tartibi'),
        ),
    ]
