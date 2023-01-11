from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from django_resized import ResizedImageField


class BaseModel(models.Model):  
    created_at = models.DateTimeField(_('Qo\'shilgan sana'), auto_now_add=True)
    updated_at = models.DateTimeField(_('O\'zgartirilgan sana'), auto_now=True)


    class Meta:
        abstract = True


class News(BaseModel):
    title = models.CharField(_('Sarlovha'), max_length=255)
    photo = ResizedImageField(_('Rasm'), size=[888, 390], crop=['middle', 'center'],
                              upload_to='news/images/%Y/%m', blank=True, null=True)
    body = RichTextField(_('Asosiy qism'))
    posted_date = models.DateTimeField(_('Post qilingan vaqt'))
    slug = models.SlugField(max_length=255,blank=True, null=True, unique=False)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ('-posted_date',)

    def __str__(self):
        return self.title



class VideoMaterials(BaseModel):
    title = models.CharField(_('Nomi'), max_length=250)
    video = models.FileField(_('Video'),upload_to='video-materials/%Y%m', null=True)
    seen = models.PositiveIntegerField(_('Ko\'rganlar soni'), default=0)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = 'Video Material'
        verbose_name_plural = 'Video Materiallar'

    def __str__(self):
        return self.title


class Material(BaseModel):
    title = models.CharField(_('Sarlavha'), max_length=250)
    files = models.FileField(blank=True, null=True, upload_to='materials/%Y/%m')
    body = RichTextField(_('Asosiy qism'))
    image = ResizedImageField(_('Rasm'), size=[888, 390], crop=['middle', 'center'],
                              upload_to='materials/images/%Y/%m', blank=True, null=True)
    downloaded = models.PositiveIntegerField(_('Ko\'chirib olganlar soni'), default=0)
    slug = models.SlugField(max_length=250, unique=True)


    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiallar'


    def __str__(self):
        return self.title



