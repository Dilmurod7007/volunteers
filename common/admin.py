from django.contrib import admin

from common import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'order']


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'order', 'active']


@admin.register(models.Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['phone', 'text']


@admin.register(models.SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ['facebook', 'instagram', 'telegram']


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'logo', 'link', 'is_active']
