from modeltranslation.translator import TranslationOptions, register
from . import models


@register(models.Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'contact_person')


@register(models.Direction)
class DirectionTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(models.RequiredSkill)
class RequiredSkillTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(models.Requirement)
class RequirementTranslationOptions(TranslationOptions):
    fields = ('title',)
