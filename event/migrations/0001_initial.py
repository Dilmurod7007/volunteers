# Generated by Django 3.2 on 2021-12-03 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('volunteer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('title_uz', models.CharField(max_length=200, null=True)),
                ('title_ru', models.CharField(max_length=200, null=True)),
                ('title_en', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name': "Yo'nalish",
                'verbose_name_plural': "Yo'nalishlar",
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Mavzu')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Mavzu')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Mavzu')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Mavzu')),
                ('description', models.TextField(verbose_name='Tavsifi')),
                ('description_uz', models.TextField(null=True, verbose_name='Tavsifi')),
                ('description_ru', models.TextField(null=True, verbose_name='Tavsifi')),
                ('description_en', models.TextField(null=True, verbose_name='Tavsifi')),
                ('starting_date', models.DateField(verbose_name='Boshlanish sanasi')),
                ('finishing_date', models.DateField(verbose_name='Tugash sanasi')),
                ('starting_time', models.TimeField(verbose_name='Boshlanish vaqti')),
                ('finishing_time', models.TimeField(verbose_name='Tugash vaqti')),
                ('volunteers_needed', models.IntegerField(verbose_name="Ko'ngillilar soni")),
                ('volunteers_will_be_paid', models.BooleanField(default=True, verbose_name="Ko'ngillilarga pul to'lanadimi?")),
                ('contact_person', models.CharField(max_length=255, verbose_name="Bog'lanish uchun shaxs")),
                ('contact_person_uz', models.CharField(max_length=255, null=True, verbose_name="Bog'lanish uchun shaxs")),
                ('contact_person_ru', models.CharField(max_length=255, null=True, verbose_name="Bog'lanish uchun shaxs")),
                ('contact_person_en', models.CharField(max_length=255, null=True, verbose_name="Bog'lanish uchun shaxs")),
                ('image', models.ImageField(upload_to='event/images/%Y/%m', verbose_name='Rasim')),
                ('is_liked', models.BooleanField(default=False, verbose_name='Yoqtirilganmi')),
                ('status', models.PositiveIntegerField(choices=[(1, 'On Moderation'), (2, 'Canceled'), (3, 'Ended'), (4, 'On Proccess')], default=1, verbose_name='Holati')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_city', to='volunteer.region', verbose_name='Shahar')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_country', to='volunteer.country', verbose_name='Davlat')),
                ('direction', models.ManyToManyField(related_name='event_direction', to='event.Direction', verbose_name="Yo'nalish")),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_region', to='volunteer.district', verbose_name='Tuman')),
                ('liked_user', models.ManyToManyField(blank=True, related_name='event_liked_users', to=settings.AUTH_USER_MODEL, verbose_name='Layk bosganlar')),
                ('oranization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_organization', to=settings.AUTH_USER_MODEL, verbose_name='Tashkilot')),
            ],
            options={
                'verbose_name': 'Tadbir',
                'verbose_name_plural': 'Tadbirlar',
            },
        ),
        migrations.CreateModel(
            name='RequiredSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('title_uz', models.CharField(max_length=250, null=True)),
                ('title_ru', models.CharField(max_length=250, null=True)),
                ('title_en', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Talab qilingan mahorat',
                'verbose_name_plural': 'Talab qilingan mahoratlar',
            },
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('title_uz', models.CharField(max_length=250, null=True)),
                ('title_ru', models.CharField(max_length=250, null=True)),
                ('title_en', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Talab',
                'verbose_name_plural': 'Talablar',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=35)),
                ('slug', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Teg',
                'verbose_name_plural': 'Teglar',
            },
        ),
        migrations.CreateModel(
            name='VolunteerForEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveIntegerField(blank=True, choices=[(1, 'On_moderation'), (2, 'Active'), (3, 'Finished')], default=1, null=True, verbose_name='Xolati')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.event', verbose_name='Tadbir')),
                ('volunteer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Valantyor')),
            ],
            options={
                'verbose_name': 'Tadbir uchun Volantyor',
                'verbose_name_plural': 'Tadbir uchun Volantyorlar',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='required_skills',
            field=models.ManyToManyField(related_name='event_required_skilss', to='event.RequiredSkill', verbose_name='Talab qilinadigan mahoratlar'),
        ),
        migrations.AddField(
            model_name='event',
            name='requirements',
            field=models.ManyToManyField(related_name='event_requirements', to='event.Requirement', verbose_name='Talablar'),
        ),
        migrations.AddField(
            model_name='event',
            name='tag',
            field=models.ManyToManyField(to='event.Tag', verbose_name='Teglar'),
        ),
    ]
