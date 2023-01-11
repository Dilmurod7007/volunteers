from django.contrib import admin
from . import models




class RequiredSkillInLine(admin.TabularInline):
    model = models.RequiredSkill
    extra = 0


class RequirementInLine(admin.TabularInline):
    model = models.Requirement
    extra = 0


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'city']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['word', 'slug']
    prepopulated_fields = {'slug': ('word',)}


admin.site.register(models.RequiredSkill)
admin.site.register(models.Requirement)
admin.site.register(models.Direction)
admin.site.register(models.VolunteerForEvent)


