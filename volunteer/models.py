from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django_resized import ResizedImageField
from rest_framework.authtoken.models import Token

from config import settings

from common.models import BaseModel, SocialNetwork, SocialNetworkAbtract


class Country(models.Model):
    name = models.CharField(_('Nomi'), max_length=64)
    code = models.CharField(_('Kodi'), max_length=8, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Davlat')
        verbose_name_plural = _('Davlatlar')


class Region(models.Model):
    name = models.CharField(_('Nomi'), max_length=64)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions', verbose_name=_('Davlat'))

    def __str__(self):
        return f'{self.country.name} - {self.name}'

    class Meta:
        verbose_name = _('Hudud')
        verbose_name_plural = _('Hududlar')


class District(models.Model):
    name = models.CharField(_('Nomi'), max_length=64)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts', verbose_name=_('Hudud'))

    def __str__(self):
        return f'{self.region.name} - {self.name}'

    class Meta:
        verbose_name = _('Tuman')
        verbose_name_plural = _('Tumanlar')


class OrganizationType(models.Model):
    name = models.CharField(_('Tashkilot turi'), max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Tashkilot turi')
        verbose_name_plural = _('Tashkilot turi')


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Siz emailga ega bo'lishingiz kerak"))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, SocialNetworkAbtract):
    USER_TYPE = (
        (1, _('Volontyor')),
        (2, _('Tashkilot')),
    )
    email = models.EmailField(_('Elektron pochta'), unique=True)
    user_type = models.IntegerField(_('Foydalanuvchi turi'), choices=USER_TYPE, blank=True, null=True)  # new added
    first_name = models.CharField(_('Ismi'), max_length=32, blank=True, null=True)
    last_name = models.CharField(_('Familiyasi'), max_length=32, blank=True, null=True)
    middle_name = models.CharField(_('Otasining ismi'), max_length=32, blank=True, null=True)
    date_of_birth = models.DateField(_('Tug\'ilgan sanasi'), blank=True, null=True)
    organization_name = models.CharField(_('Nomi'), max_length=256, blank=True, null=True)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.CASCADE,
                                          verbose_name=_('Tashkilot turi'), blank=True, null=True)
    person_for_contact = models.CharField(_('Bog\'lanish uchun shaxs'), max_length=64, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True,
                                null=True, related_name='country', verbose_name=_('Davlat'))  # korish kerak
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='region', verbose_name=_('Hudud'))
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='district', verbose_name=_('Tuman'))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=_(
                                     "Quyidagi formatda kiritishingiz kerak: '+999999999'. 15 raqamgacha ruxsat etiladi"))
    phone = models.CharField(_('Telefon raqam'), max_length=60, validators=[phone_regex], null=True, blank=True)
    photo = ResizedImageField(_('Rasm'), size=[500, 500], crop=['middle', 'center'], upload_to='volunteer/images/%Y/%m',
                              blank=True, null=True)
    about = models.TextField(_('Ta\'rif'), blank=True, null=True)
    is_staff = models.BooleanField(_('Xodimmi'), default=False)
    is_active = models.BooleanField(_('Faolmi'), default=False)
    created_at = models.DateTimeField(_('Yaratilgan sana'), auto_now_add=True)
    updated_at = models.DateTimeField(_('O\'zgartirilgan sana'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_full_name(self):
        if self.first_name and self.last_name and self.middle_name:
            return f'{self.last_name} {self.first_name} {self.middle_name}'
        if self.organization_name:
            return self.organization_name
        else:
            return self.email

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar')
        ordering = ['-created_at']


class UserEmailCode(models.Model):
    email = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.email} uchun kod'

    class Meta:
        verbose_name = _('Emailga yuborilgan kod')
        verbose_name_plural = _('Emailga yuborilgan kodlar')
        ordering = ['-date_created']


class Language(models.Model):
    name = models.CharField(_('Nomi'), max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Til')
        verbose_name_plural = _('Tillar')


class Goal(models.Model):
    name = models.CharField(_('Nomi'), max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Maqsad')
        verbose_name_plural = _('Maqsadlar')


class UserProfile(BaseModel):
    EDUCATION_LEVEL = (
        (1, _("O'rta")),
        (2, _("O'rta maxsus")),
        (3, _('Bakalavr')),
        (4, _('Magistr')),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Foydalanuvchi'), related_name='profile')
    about_me = models.TextField(_("O'zingiz haqingizda"), blank=True, null=True)
    education_level = models.PositiveIntegerField(_("Ma'lumoti"), choices=EDUCATION_LEVEL, default=1)
    specialty = models.CharField(_("Mutaxassisligi"), max_length=64, blank=True, null=True)
    languages = models.ManyToManyField(Language, verbose_name=_('Til'),
                                  related_name='volunteer_profile', blank=True)
    interests = models.CharField(_('Qiziqishalar'), max_length=128, blank=True, null=True)
    goals = models.ManyToManyField(Goal, verbose_name=_('Maqsad'), related_name='volunteer_profile', blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} profile"

    class Meta:
        verbose_name = _('Foydalanuvchi profili')
        verbose_name_plural = _('Foydalanuvchilar profili')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class VolunteerRating(BaseModel):
    VOLUNTEER_RATING = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five')
    )
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Volontyor'), related_name='rating')
    organization = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Tashkilot'))
    rating = models.PositiveIntegerField(_('Reytinggi'), choices=VOLUNTEER_RATING, default=5)

    def __str__(self):
        return f'{self.organization.organization_name} {self.volunteer.get_full_name()} ni {self.rating} bilan baholadi'

    class Meta:
        verbose_name = _('Volontyor reytinggi')
        verbose_name_plural = _('Volontyorlar reytinggi')
        unique_together = ['volunteer', 'organization']
