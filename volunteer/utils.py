from random import randint

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _


class Util:
    @staticmethod
    def sending_email(to, code=None):
        subject = _("Hisobni faollashtirish")
        msg = _(f"Iltimos ro'yxatdan o'tish uchun ushbu kodni kiriting: {code}")
        if to and code:
            try:
                send_mail(subject, msg, settings.EMAIL_HOST_USER, [to], fail_silently=False)
            except BadHeaderError:
                return Response(_('Xato header topildi'))
            data = {
                'email': to,
                'message': _('Email muvaffaqiyatli yuborildi')
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            msg = _("Maydonlar to'g'ri to'ldirilganligiga ishonch hosil qiling")
            return Response({'error_message': msg})

    @staticmethod
    def code_generator():
        random_num = randint(100000, 999999)
        return random_num
