from modeltranslation.translator import TranslationOptions, register
from . import models


@register(models.OrganizationType)
class OrganizationTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(models.Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(models.Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(models.District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(models.User)
class UserTranslationOptions(TranslationOptions):
    fields = ('about',)


@register(models.Goal)
class GoalTranslationOptions(TranslationOptions):
    fields = ('name',)
