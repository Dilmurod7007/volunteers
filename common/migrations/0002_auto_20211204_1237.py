# Generated by Django 3.2.9 on 2021-12-04 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='footer',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='is_static',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='okru',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='rss',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='twitter',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='vkontakte',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='youtube',
        ),
        migrations.AlterField(
            model_name='menu',
            name='link',
            field=models.CharField(max_length=500, null=True, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Tartibi'),
        ),
    ]
