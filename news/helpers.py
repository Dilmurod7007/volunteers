import os
from django.conf import settings
from django.db.models import ManyToManyField
from django.utils.text import slugify
from sorl.thumbnail import get_thumbnail
from datetime import timedelta as td, datetime
from transliterate import translit, get_available_language_codes







def generate_unique_slug(klass, field, instance=None):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    translated = translit(field, 'ru', reversed=True)
    origin_slug = slugify(translated)
    unique_slug = origin_slug
    numb = 1
    if instance:
        queryset = klass.objects.exclude(id=instance).filter(slug=unique_slug)
    else:
        queryset = klass.objects.filter(slug=unique_slug)

    while queryset.exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


# UPDATING INSTANCE'S MODEL VALUES WITH GIVEN DICT
def update_object_values(obj, dict):  # requires object and dictionary. Set values to the object
    manytomany_fields = ['department']
    image_list = ['image', 'icon', 'photo', 'background_image']
    for attr, value in dict.items():

        if hasattr(obj, attr):
            if attr in image_list and attr is None:
                print(attr, 'alalalalalalla')
                pass
            else:
                setattr(obj, attr, value)

    obj.save()


# GENERATING UNIQUE ID
# def unique_number_generator(klass, length, attribute='order_number'):
def unique_number_generator(klass, length, instance, type):
    last_id = klass.objects.filter(order_number__startswith=type).exclude(id=instance.id).order_by('id').last()

    if not last_id or not last_id.order_number:  # return initial number
        initial = (length - 1) * "0" + '1'
        return initial

    number = last_id.order_number
    number = number.replace(type, '')

    number = int(number) + 1
    formatted = (length - len(str(number))) * "0" + str(number)
    return str(formatted)


# CHECK WHETHER APARTMENT IS ALREADY EXISTS

# def is_object_exists(klass, choice, unique_number, apartment=None, house=None):
#     """
#     NOTE:
#         We have divided into 2 choices. 1-House, 2-Apartment
#         If HOUSE first logic will run
#         If APARTMENT the second logic will run
#
#     """
#     if choice == 'house':
#         department = klass.objects.get(id=unique_number).department
#         return klass.objects.filter(house_number=unique_number, department=department).exists()
#     elif choice == 'apartment':
#         pass
#         # return klass.objects.filter(house_number=unique_number, department=).exists()
#     pass


def area_range_validator(tariff):
    for index, tariff_item in enumerate(tariff):
        start = int(tariff_item.get('from_area'))
        end = int(tariff_item.get('to_area'))
        if start > end:
            return 0

        for index2, item in enumerate(tariff):
            if not index == index2:
                from_area = int(item.get('from_area'))
                to_area = int(item.get('to_area'))
                if from_area in range(start, end) or to_area in range(start, end):
                    return 1


# IMAGE SIZE GENERATOR
def image_size_generator(image, custom=None):
    size = {
        "default": '%s%s' % (settings.HOST, image.url),
        "large": '%s%s' % (settings.HOST, get_thumbnail(image, '1024x768', crop='center', quality=90).url),
        "medium": '%s%s' % (settings.HOST, get_thumbnail(image, '900x530', crop='center', quality=90).url),
        "small": '%s%s' % (settings.HOST, get_thumbnail(image, '230x322', crop='center', quality=90).url),
    }

    if custom:
        for item in custom:
            size[item] = '%s%s' % (settings.HOST, get_thumbnail(image, item, crop='center', quality=90).url),

    return size


def avatar_image_size_generator(image):
    size = {
        "default": '%s%s' % (settings.HOST, image.url),
        "large": '%s%s' % (settings.HOST, get_thumbnail(image, '126x126', crop='center', quality=90).url),
        "medium": '%s%s' % (settings.HOST, get_thumbnail(image, '80x80', crop='center', quality=90).url),
        "small": '%s%s' % (settings.HOST, get_thumbnail(image, '44x44', crop='center', quality=90).url),
    }
    return size


# IMAGE SIZE GENERATOR
def news_thumbnail_image_size_generator(image, custom=None):
    a = ('273x178',
         '580x515',
         '66x66',
         '392x343',
         '245x268',
         '131x116',
         '580x472',
         '274x220',
         '376x274',
         '274x150',
         '408x303',
         '274x150',
         '274x194',
         '580x316')

    size = {
        "default": '%s%s' % (settings.HOST, image.url),
        "xlarge": '%s%s' % (settings.HOST, get_thumbnail(image, '580x515', crop='center', quality=90).url),
        "large": '%s%s' % (settings.HOST, get_thumbnail(image, '580x316', crop='center', quality=90).url),
        "xmedium": '%s%s' % (settings.HOST, get_thumbnail(image, '274x220', crop='center', quality=90).url),
        "medium": '%s%s' % (settings.HOST, get_thumbnail(image, '274x220', crop='center', quality=90).url),
        "small": '%s%s' % (settings.HOST, get_thumbnail(image, '274x194', crop='center', quality=90).url),
        "xsmall": '%s%s' % (settings.HOST, get_thumbnail(image, '116x86', crop='center', quality=90).url),
    }

    if custom:
        for item in custom:
            size[item] = '%s%s' % (settings.HOST, get_thumbnail(image, item, crop='center', quality=90).url),

    return size


# IMAGE SIZE GENERATOR
def image_size_generator_from_path(image, custom=None):
    image_file = open(os.path.join(settings.MEDIA_ROOT, image))
    size = {
        "default": '%s%s%s' % (settings.HOST, settings.MEDIA_URL, image),
        "large": '%s%s' % (settings.HOST, get_thumbnail(image_file, '1024x768', crop='center', quality=90).url),
        "medium": '%s%s' % (settings.HOST, get_thumbnail(image_file, '900x530', crop='center', quality=90).url),
        "small": '%s%s' % (settings.HOST, get_thumbnail(image_file, '230x322', crop='center', quality=90).url),
    }

    if custom:
        for item in custom:
            size[item] = '%s%s' % (settings.HOST, get_thumbnail(image, item, crop='center', quality=90).url),

    return size


# IMAGE SIZE GENERATOR
def profile_image_size_generator_from_path(image, custom=None):
    image_file = open(os.path.join(settings.MEDIA_ROOT, image))
    size = {
        "default": '%s%s%s' % (settings.HOST, settings.MEDIA_URL, image),
        "large": '%s%s' % (settings.HOST, get_thumbnail(image_file, '44x44', crop='center', quality=90).url),
        "medium": '%s%s' % (settings.HOST, get_thumbnail(image_file, '80x80', crop='center', quality=90).url),
        "small": '%s%s' % (settings.HOST, get_thumbnail(image_file, '96x96', crop='center', quality=90).url),
    }

    if custom:
        for item in custom:
            size[item] = '%s%s' % (settings.HOST, get_thumbnail(image, item, crop='center', quality=90).url),

    return size


# TIME RANGE CALCULATOR
def get_delta(start_date, end_date):
    start = str(start_date)
    end = str(end_date)
    d1 = start.strptime(start_date, '%Y-%m-%d %H:%M')
    d2 = end.strptime(end_date, '%Y-%m-%d %H:%M')
    delta = d2 - d1
    return delta
