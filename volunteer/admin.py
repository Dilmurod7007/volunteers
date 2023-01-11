from django.contrib import admin

from .models import User, Country, Region, District, OrganizationType, UserEmailCode, VolunteerRating, UserProfile, \
    Language, Goal


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'user_type', 'created_at', 'is_active']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']


@admin.register(District)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region']


@admin.register(UserEmailCode)
class UserEmailCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'code']


@admin.register(OrganizationType)
class UserEmailCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(VolunteerRating)
class VolunteerRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'volunteer', 'organization', 'rating']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
