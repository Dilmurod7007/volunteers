# Generated by Django 3.2.9 on 2021-12-09 05:06

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0012_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='our_mission',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Bizning maqsad'),
        ),
    ]
