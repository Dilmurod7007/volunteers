from django.utils import timezone

from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from django_resized import ResizedImageField


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Kiritilgan sana'), auto_now_add=True)
    updated_at = models.DateTimeField(_('O\'zgartirilgan sana'), auto_now=True)

    class Meta:
        abstract = True


class Menu(BaseModel):
    title = models.CharField(_('Nomi'), max_length=256)
    link = models.CharField(_('Link'), max_length=512, blank=True, null=True)
    order = models.PositiveIntegerField(_('Tartibi'), default=1)  # ozgarishi mumkin
    is_right = models.BooleanField(_("Header o'ng tarafga"), default=False)
    slug = models.SlugField(_('Slag'), blank=True)
    is_active = models.BooleanField(_('Faolmi'), default=False)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            slug = slugify(self.title)
            return super(Menu, self).save()


# SOCIAL NETWORKS
class SocialNetwork(BaseModel):
    facebook = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = _('Ijtimoiy tarmoqlar')
        verbose_name_plural = _('Ijtimoiy tarmoqlar')

    def __str__(self):
        return f"Ijtimoiy tarmoqlar"


# SOCIAL NETWORKS
class SocialNetworkAbtract(models.Model):
    facebook = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True


class Settings(SocialNetworkAbtract):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_(
        "Quyidagi formatda kiritishingiz kerak: '+999999999'. 15 raqamgacha ruxsat etiladi"))
    phone = models.CharField(_('Telefon raqam'), max_length=16, validators=[phone_regex], null=True, blank=True)
    text = models.TextField(_('Matn'), blank=True, null=True)
    additional_link = models.CharField(_("qo'shimcha link"), blank=True, null=True, max_length=512)
    aphorism = models.CharField(_('Aforizm'), max_length=512, blank=True, null=True)
    our_mission = RichTextField(_('Bizning maqsad'), blank=True, null=True)

    def __str__(self):
        return "Sayt uchun kerakli ma'lumotlar"

    class Meta:
        verbose_name = _('Sayt Sozlamalari')
        verbose_name_plural = _('Sayt Sozlamalari')


class Slider(BaseModel):
    title = models.CharField(_('Sarlavha'), max_length=256)
    text = RichTextField(_('Matn'))
    photo = ResizedImageField(_('Rasm'), size=[1440, 680], crop=['middle', 'center'], upload_to='slider/images/%Y/%m',
                              blank=True, null=True)
    link = models.CharField(_('Link'), max_length=512, blank=True, null=True)
    active = models.BooleanField(_('Faol'), default=False)
    order = models.PositiveIntegerField(_('Tartibi'), default=1)
    is_right = models.BooleanField(_("O'ngdami"), default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Slayder")
        verbose_name_plural = _('Slayderlar')


class Partner(BaseModel):
    name = models.CharField(_('Nomi'), max_length=64)
    logo = ResizedImageField(_('Rasm'), size=[500, 500], crop=['middle', 'center'], upload_to='partner/images/%Y/%m',
                             blank=True, null=True)
    link = models.CharField(_('Websayt'), max_length=512, blank=True, null=True)
    order = models.PositiveIntegerField(_('Tartibi'), default=1)
    is_active = models.BooleanField(_('Faolmi'), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Hamkor')
        verbose_name_plural = _('Hamkorlar')


# STATIC PAGE
class Page(BaseModel):
    title = models.CharField(_('Sahifa nomi'), max_length=200)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    content = RichTextField(_('Batafsil'))
    date = models.DateTimeField(_('Vaqti'), default=timezone.now)
    active = models.BooleanField(_('Faol'), default=False)

    class Meta:
        verbose_name = _('Sahifa')
        verbose_name_plural = _('Sahifalar')
        ordering = ['-date']

    def __str__(self):
        return self.title
