from modeltranslation.translator import TranslationOptions, register
from . import models


@register(models.Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(models.Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(models.Settings)
class SettingsTranslationOptions(TranslationOptions):
    fields = ('text', 'aphorism', 'our_mission')
