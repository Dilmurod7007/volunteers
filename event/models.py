from django.db import models
from django.utils.translation import ugettext_lazy as _



class Tag(models.Model):
    word = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Teg'
        verbose_name_plural = 'Teglar'

    def __str__(self):
        return self.word


class Direction(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Yo\'nalish'
        verbose_name_plural = 'Yo\'nalishlar'

    def __str__(self):
        return self.title


class Event(models.Model):

    class EventStatus(models.IntegerChoices):
        active = 1, _('Active')
        finished = 2, _('Finished')
        canceled = 3, _('Bekorqilingan')


    title = models.CharField(_('Mavzu'), max_length=255)
    oranization = models.ForeignKey('volunteer.User', on_delete=models.CASCADE, verbose_name=_('Tashkilot'),
                                    related_name='event_organization')
    country = models.ForeignKey('volunteer.Country', on_delete=models.SET_NULL, verbose_name=_('Davlat'),
                                related_name='event_country', null=True, blank=True)
    city = models.ForeignKey('volunteer.Region', on_delete=models.SET_NULL, verbose_name=_('Shahar'),
                             related_name='event_city', null=True, blank=True)
    district = models.ForeignKey('volunteer.District', on_delete=models.SET_NULL, verbose_name=_('Tuman'),
                                 related_name='event_region', null=True, blank=True)
    requirements = models.ManyToManyField('Requirement', verbose_name=_('Talablar'), related_name='event_requirements')
    required_skills = models.ManyToManyField('RequiredSkill', verbose_name=_('Talab qilinadigan mahoratlar'),
                                             related_name='event_required_skilss')
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(_('Tavsifi'))
    starting_date = models.DateField(_('Boshlanish sanasi'))
    finishing_date = models.DateField(_('Tugash sanasi'))
    starting_time = models.TimeField(_('Boshlanish vaqti'))
    finishing_time = models.TimeField(_('Tugash vaqti'))
    direction = models.ManyToManyField(Direction, verbose_name=_('Yo\'nalish'), related_name='event_direction')
    volunteers_needed = models.IntegerField(_('Ko\'ngillilar soni'))
    volunteers_will_be_paid = models.BooleanField(_('Ko\'ngillilarga pul to\'lanadimi?'), default=True)
    contact_person = models.CharField(_('Bog\'lanish uchun shaxs'), max_length=255)
    image = models.ImageField(_('Rasim'), upload_to='event/images/%Y/%m')
    liked_user = models.ManyToManyField('volunteer.User', verbose_name=_('Layk bosganlar'),
                                        related_name='event_liked_users', blank=True)
    is_liked = models.BooleanField(default=False, blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name=_('Teglar'))
    status = models.PositiveIntegerField(_('Xolati'), default=EventStatus.active,
                                         choices=EventStatus.choices, blank=True, null=True)
    created_date = models.DateTimeField(_('Yaratilgan sana'), auto_now_add=True)

    class Meta:
        verbose_name = 'Tadbir'
        verbose_name_plural = 'Tadbirlar'

    def __str__(self):
        return self.title


class RequiredSkill(models.Model):
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Talab qilingan mahorat'
        verbose_name_plural = 'Talab qilingan mahoratlar'

    def __str__(self):
        return self.title


class Requirement(models.Model):
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Talab'
        verbose_name_plural = 'Talablar'

    def __str__(self):
        return self.title


class VolunteerStatus(models.IntegerChoices):
    registered = 1, _('Registered')
    canceled = 2, _('Canceled')


class VolunteerForEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_('Tadbir'), blank=True, null=True)
    volunteer = models.ForeignKey('volunteer.User', on_delete=models.SET_NULL, verbose_name=_('Valantyor'), blank=True,
                                  null=True)
    status = models.PositiveIntegerField(_('Xolati'), default=VolunteerStatus.registered,
                                         choices=VolunteerStatus.choices, blank=True, null=True)

    class Meta:
        verbose_name = "Tadbir uchun Volantyor"
        verbose_name_plural = "Tadbir uchun Volantyorlar"

    def __str__(self):
        return f'{str(self.volunteer.email)}  {str(self.event)} uchun'
