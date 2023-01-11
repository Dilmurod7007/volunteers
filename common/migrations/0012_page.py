# Generated by Django 3.2.9 on 2021-12-08 12:42

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_slider_is_right'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Kiritilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('title', models.CharField(max_length=200, verbose_name='Sahifa nomi')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('content', ckeditor.fields.RichTextField(verbose_name='Batafsil')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Vaqti')),
                ('active', models.BooleanField(default=False, verbose_name='Faol')),
            ],
            options={
                'verbose_name': 'Sahifa',
                'verbose_name_plural': 'Sahifalar',
                'ordering': ['-date'],
            },
        ),
    ]