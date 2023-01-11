from django.contrib import admin
from news import models


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'posted_date']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.VideoMaterials)
class VieoMaterialsAdmin(admin.ModelAdmin):
    list_display = ['title', 'video', 'seen', ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Material)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}


