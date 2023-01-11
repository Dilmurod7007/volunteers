# Generated by Django 3.2.9 on 2021-12-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20211204_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='is_activa',
            field=models.BooleanField(default=True, verbose_name='Faolmi'),
        ),
        migrations.AddField(
            model_name='partner',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Faolmi'),
        ),
        migrations.AddField(
            model_name='settings',
            name='aphorism',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Aforizm'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='link',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='Tartibi'),
        ),
    ]