# Generated by Django 3.2.9 on 2021-12-05 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20211205_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialnetwork',
            name='youtube',
            field=models.URLField(blank=True, null=True),
        ),
    ]