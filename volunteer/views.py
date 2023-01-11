from datetime import date, datetime, timezone
from django.contrib.auth import logout
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListCreateAPIView, UpdateAPIView, get_object_or_404, DestroyAPIView
from rest_framework.views import APIView

from common.serializers import UserEventSerializer, VolunteerLikedEventSerializer
from event.models import VolunteerForEvent, Event
from event.views import check_liked_and_check_status
from .models import User, UserEmailCode, VolunteerRating
from .pagination import CustomPagination, EventVolunteersPagination
from .serializers import EmailInputSerializer, UserEmailCodeSerializer, VolunteerRegisterSerializer, \
    OrganizationRegisterSerializer, VolunteerProfileUpdateSerializer, UserPasswordResetSerializer, \
    OrganizationProfileUpdateSerializer, VolunteerForMapSerializer, GiveRatingSerializer, VolunteerInfoSerializer
from .utils import Util

from django.utils.translation import ugettext_lazy as _


# COMMON LIST
class MyListApiView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# COMMON API DETAIL VIEW
class MyDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyUpdateApiView(UpdateAPIView):

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class MyDestroyApiView(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyCreateAPIView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SendCodeToEmailAPIView(CreateAPIView):
    serializer_class = EmailInputSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        email = user_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
            pass
        if user:
            return Response({'error_message': _(
                'Tizimda ushbu emailga ega bo\'lgan foydalanuvchi mavjud!!!')})  # status qoshish kerak
        else:
            try:
                user_email_code_instance = UserEmailCode.objects.get(email=email)
            except UserEmailCode.DoesNotExist:
                user_email_code_instance = None
                pass
            code = Util.code_generator()
            if user_email_code_instance:
                user_email_code_instance.code = code
                user_email_code_instance.save()
            else:
                UserEmailCode.objects.create(email=email, code=code)
            Util.sending_email(email, code)
            return Response(serializer.data, status=status.HTTP_200_OK)  # korish kerak


class CodeVerification(APIView):
    def post(self, request, *args, **kwargs):
        user_input_code = str(request.data['code'])
        email = request.data['email']
        try:
            user_code_instance = get_object_or_404(UserEmailCode, email=email)
        except:
            user_code_instance = None
            pass
        if user_code_instance.code == user_input_code:
            user_code_instance.is_active = True
            user_code_instance.save()
            data = {
                'email': email,
                'is_verified': True
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error_message': _('Kiritilgan kod noto\'g\'ri!!!')}
            )


class ReSendCodeAPIView(APIView):

    def get(self, request, *args, **kwargs):
        email = request.data['email']
        try:
            user_code_instance = UserEmailCode.objects.get(email=email)
        except UserEmailCode.DoesNotExist:
            user_code_instance = None
            pass
        if user_code_instance:
            if user_code_instance.updated_date:
                code_created_data = user_code_instance.updated_date
            else:
                code_created_data = user_code_instance.date_created
            now = datetime.now(timezone.utc)
            time_delta = now - code_created_data
            total_seconds = time_delta.total_seconds()
            if total_seconds < 240:
                remain_seconds = 240 - total_seconds
                return Response({'message': _(f'Siz {remain_seconds} sekunddan keyin qayta jo\'nata olasiz!!!')})
            else:
                new_code = Util.code_generator()
                Util.sending_email(to=email, code=new_code)
                user_code_instance.code = new_code
                user_code_instance.save()
        else:
            new_code = Util.code_generator()
            Util.sending_email(to=email, code=new_code)
            UserEmailCode.objects.create(email=email, code=new_code)
        msg = _('Sizga kod qayta yuborildi!!!')
        data = {
            'email': email,
            'info_message': msg
        }
        return Response(data, status=status.HTTP_200_OK)


class VolunteerRegisterAPIView(MyCreateAPIView):
    serializer_class = VolunteerRegisterSerializer
    queryset = User.objects.all()


class OrganizationRegisterAPIView(MyCreateAPIView):
    serializer_class = OrganizationRegisterSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        error_message = _("Siz ro'yxatdan o'tmagansiz, Iltimos ro'yxatdan o'ting!!!")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error_message': error_message}, status=status.HTTP_404_NOT_FOUND)
        token = Token.objects.get_or_create(user=user)[0]
        if user.check_password(password) is False:
            raise ValidationError({"message": _("Noto'g'ri parol kiritdingiz")})
        if user:
            if user.is_active:
                return Response({
                    'email': email,
                    'token': token.key,
                    'user_type': user.user_type
                })
            else:
                raise ValidationError({'error_message': _('Hisob faol emas')})
        else:
            raise ValidationError({'error_message': _('Hisob mavjud emas')})


class UserLogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response({'success_message': _('Siz hisobdan muvaffaqiyatli chiqdingiz!!!')})


class VolunteerProfileUpdateView(MyDetailAPIView, MyUpdateApiView):
    serializer_class = VolunteerProfileUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        object = User.objects.get(pk=self.request.user.pk)
        return object


class OrganizationProfileUpdateView(MyDetailAPIView, MyUpdateApiView):
    serializer_class = OrganizationProfileUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        object = User.objects.get(pk=self.request.user.pk)
        return object


class PasswordResetView(MyUpdateApiView):
    serializer_class = UserPasswordResetSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


class UserEmailCodeAPIVIew(ListCreateAPIView):
    serializer_class = UserEmailCodeSerializer
    queryset = UserEmailCode.objects.all()


class VolunteerEventsView(MyListApiView):
    serializer_class = UserEventSerializer
    queryset = VolunteerForEvent.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        volunteer = self.request.user
        volunteer_events_id = self.queryset.filter(
            volunteer=volunteer, status=1).values_list('event', flat=True)
        volunteer_events = Event.objects.filter(id__in=volunteer_events_id)
        volunteer_liked_events_queryset = Event.objects.filter(liked_user__in=[request.user.pk, ])
        volunteer_liked_events = VolunteerLikedEventSerializer(volunteer_liked_events_queryset, context=context,
                                                               many=True).data

        volunteer_events_active_queryset = volunteer_events.filter(status=1)
        volunteer_events_ended_queryset = volunteer_events.filter(status=2)

        volunteer_events_active = self.get_serializer(volunteer_events_active_queryset, context=context, many=True).data
        volunteer_events_finished = self.get_serializer(volunteer_events_ended_queryset, context=context,
                                                        many=True).data

        volunteer_events = {
            'volunteer_events_active': volunteer_events_active,
            'volunteer_events_finished': volunteer_events_finished,
            'volunteer_liked_events': volunteer_liked_events
        }

        return Response(volunteer_events, status=status.HTTP_200_OK)


class OrganizationEventsView(MyListApiView):
    serializer_class = UserEventSerializer
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        user = self.request.user
        organization_events = Event.objects.filter(oranization=user)

        organization_events_active_queryset = organization_events.filter(status=1)
        organization_events_ended_queryset = organization_events.filter(status=2)

        organization_events_active = self.get_serializer(organization_events_active_queryset, context=context,
                                                         many=True).data
        organization_events_finished = self.get_serializer(organization_events_ended_queryset, context=context,
                                                           many=True).data

        organization_events = {
            'organization_events_active': organization_events_active,
            'organization_events_finished': organization_events_finished,
        }

        return Response(organization_events, status=status.HTTP_200_OK)


class EventVolunteersListView(MyListApiView):
    serializer_class = VolunteerForMapSerializer
    queryset = User.objects.all()
    pagination_class = EventVolunteersPagination
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ('id', 'first_name', 'last_name')

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        pk = kwargs.get('pk')
        event = Event.objects.get(pk=pk)
        event_volunteers_id = VolunteerForEvent.objects.filter(event=event).values_list('volunteer', flat=True)
        event_volunteers_queryset = User.objects.filter(id__in=event_volunteers_id)
        page_data = self.paginate_queryset(self.filter_queryset(event_volunteers_queryset))
        event_volunteers = self.get_serializer(page_data, context=context, many=True).data
        volunteers = {
            'event_volunteers': event_volunteers
        }
        return self.get_paginated_response(volunteers)


class GiveRatingView(MyCreateAPIView, MyUpdateApiView, MyDetailAPIView):
    serializer_class = GiveRatingSerializer
    queryset = VolunteerRating.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        volunteer = User.objects.get(pk=pk)
        serializer = GiveRatingSerializer(data=self.request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save(organization=self.request.user, volunteer=volunteer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        volunteer_id = kwargs.get('pk')
        instance = VolunteerRating.objects.get(volunteer=volunteer_id, organization=self.request.user)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, volunteer_id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, volunteer_id):
        serializer.save(organization=self.request.user, volunteer_id=volunteer_id)


class EventVolunteerInfoView(MyDetailAPIView, MyDestroyApiView):
    serializer_class = VolunteerProfileUpdateSerializer # o'zgarishi mumkin
    queryset = User.objects.filter(user_type=1)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        volunteer_id = self.kwargs.get('volunteer_id')
        return self.queryset.get(pk=volunteer_id)

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        event_id = self.kwargs.get('pk')

        volunteer_info = self.get_serializer(self.get_object(), context=context).data

        volunteer_events_id = VolunteerForEvent.objects.filter(
            volunteer=self.get_object(), status=1).values_list('event', flat=True)

        volunteer_events = Event.objects.filter(id__in=volunteer_events_id).exclude(id=event_id)

        check_liked_and_check_status(self.request.user, volunteer_events)

        volunteer_events_active_queryset = volunteer_events.filter(status=1)
        volunteer_events_ended_queryset = volunteer_events.filter(status=2)

        volunteer_events_active = UserEventSerializer(volunteer_events_active_queryset, context=context, many=True).data
        volunteer_events_finished = UserEventSerializer(volunteer_events_ended_queryset, context=context,
                                                        many=True).data

        payload = {
            'volunteer_info': volunteer_info,
            'volunteer_events_active': volunteer_events_active,
            'volunteer_events_finished': volunteer_events_finished
        }
        return Response(payload, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        volunteer_id = self.kwargs.get('volunteer_id')
        event_id = self.kwargs.get('pk')
        instance = VolunteerForEvent.objects.get(volunteer=volunteer_id, event=event_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VolunteersList(MyListApiView):
    serializer_class = VolunteerInfoSerializer
    queryset = User.objects.filter()
    pagination_class = EventVolunteersPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('id', 'first_name', 'last_name')
    filter_fields = ('region', 'district')

    def get_queryset(self):
        return self.queryset.filter(user_type=1, country=1)

    def filter_queryset(self, queryset):
        gte_date = self.request.query_params.get('gte_date')
        lte_date = self.request.query_params.get('lte_date')
        if gte_date is None:
            if lte_date is None:
                queryset = queryset
            else:
                lte_date = datetime.strptime(lte_date, "%Y-%m-%d").date()
                queryset = queryset.filter(date_of_birth__lte=lte_date)
        else:
            gte_date = datetime.strptime(gte_date, "%Y-%m-%d").date()
            if lte_date is None:
                queryset = queryset.filter(date_of_birth__gte=gte_date)
            else:
                lte_date = datetime.strptime(lte_date, "%Y-%m-%d").date()
                queryset = queryset.filter(date_of_birth__range=[gte_date, lte_date])
        return queryset

    def get(self, request, *args, **kwargs):
        context = {'request': self.request}
        page = self.filter_queryset(
            self.get_queryset().annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating'))
        page = self.paginate_queryset(page)
        serializer = self.get_serializer(page, context=context, many=True)
        return self.get_paginated_response(serializer.data)


class VolunteerDetailView(MyDetailAPIView):
    serializer_class = VolunteerProfileUpdateSerializer
    queryset = User.objects.filter(user_type=1)
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        instance = self.get_object()
        user_data = self.get_serializer(instance).data

        volunteer_events_id = VolunteerForEvent.objects.filter(
            volunteer=self.get_object(), status=1).values_list('event', flat=True)

        volunteer_events = Event.objects.filter(id__in=volunteer_events_id)

        check_liked_and_check_status(self.get_object(), volunteer_events)

        volunteer_events_active_queryset = volunteer_events.filter(status=1)
        volunteer_events_ended_queryset = volunteer_events.filter(status=2)

        volunteer_events_active = UserEventSerializer(volunteer_events_active_queryset, context=context, many=True).data
        volunteer_events_finished = UserEventSerializer(volunteer_events_ended_queryset, context=context,
                                                        many=True).data
        payload = {
            'user_data': user_data,
            'volunteer_events_active': volunteer_events_active,
            'volunteer_events_finished': volunteer_events_finished
        }

        return Response(payload, status=status.HTTP_200_OK)
