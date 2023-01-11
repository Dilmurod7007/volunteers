from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from common import models
from common import serializers
from common.serializers import AboutPageSerializer
from event.models import Event
from event.views import check_liked_and_check_status
from volunteer.models import User
from news import models as news_models
from news import serializers as news_serializers
from volunteer import serializers as volunteer_serializers
from volunteer.serializers import VolunteerForMapSerializer, OrganizationForMapSerializer


class MyListApiView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class MainPageView(MyListApiView):
    serializer_class = serializers.MainPageSerializer
    queryset = models.Menu.objects.all()

    def get(self, request, *args, **kwargs):
        context = {'request': request}

        sliders = serializers.SliderSerializer(models.Slider.objects.filter(active=True), many=True).data

        last_events = Event.objects.all().order_by('status', '-starting_date')[:6]

        check_liked_and_check_status(request.user, last_events)

        last_events = serializers.UserEventSerializer(last_events, context=context, many=True).data

        partners = serializers.PartnerSerializer(models.Partner.objects.filter(is_active=True), many=True,
                                                 context=context).data

        last_news = news_serializers.NewsSerializer(
            news_models.News.objects.order_by('-posted_date')[:4], context=context, many=True).data

        organizations = volunteer_serializers.MainPageOrganizationSerializer(
            User.objects.filter(user_type=2).order_by('-created_at')[:4], context=context, many=True).data

        volunteers = volunteer_serializers.MainPageVolunteerSerializer(
            User.objects.filter(user_type=1).order_by('-created_at')[:6], context=context,
            many=True).data

        number_all_vols = User.objects.filter(user_type=1).count()
        number_all_orgs = User.objects.filter(user_type=2).count()
        # exclude cancelled events
        number_events = Event.objects.filter(status__in=(1, 2)).count()

        numbers = {
            'number_all_volunteers': number_all_vols,
            'number_all_organizations': number_all_orgs,
            'number_events': number_events
        }

        payload = {
            'sliders': sliders,
            'last_news': last_news,
            'last_events': last_events,
            'organizations': organizations,
            'volunteers': volunteers,
            'partners': partners,
            'numbers': numbers
        }
        return Response(payload, status=status.HTTP_200_OK)


class CommonPartListView(MyListApiView):
    serializer_class = serializers.CommonPartSerializer
    queryset = models.Settings.objects.all()
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        header = serializers.HeaderSerializer(models.Settings.objects.last()).data

        menu = serializers.MenuSerializer(models.Menu.objects.filter(is_active=True), many=True).data

        advertisements = serializers.SliderSerializer(models.Slider.objects.filter(active=True, is_right=True),
                                                      many=True).data

        user = User.objects.get(email=request.user.email)
        if user.user_type == 1:
            user_data = serializers.VolunteerProfileDataSerializer(user, context=context).data
        else:
            user_data = serializers.OrganizationProfileDataSerializer(user, context=context).data

        header = {
            'user_data': user_data,
            'menu': menu,
            'data': header,
            'advertisements': advertisements
        }
        footer = serializers.FooterSerializer(models.Settings.objects.last()).data
        common_part_data = {
            'header': header,
            'footer': footer
        }
        return Response(common_part_data, status=status.HTTP_200_OK)


class MainPageMapVolunteersListView(MyListApiView):
    serializer_class = VolunteerForMapSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('region',)
    search_fields = ('first_name', 'last_name', 'id')

    def get_queryset(self):
        return self.queryset.filter(user_type=1, country=1)

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        volunteers = self.get_serializer(self.filter_queryset(self.get_queryset()), context=context, many=True).data
        number_volunteers_uzb = self.get_queryset().count()

        data = {
            'volunteers': volunteers,
            'number_volunteers_uzb': number_volunteers_uzb,
        }
        return Response(data, status=status.HTTP_200_OK)


class MainPageMapOrganizationsListView(MyListApiView):
    serializer_class = OrganizationForMapSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('region',)
    search_fields = ('id', 'organization_name')

    def get_queryset(self):
        return self.queryset.filter(user_type=2, country=1)

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        organizations = self.get_serializer(self.filter_queryset(self.get_queryset()), context=context, many=True).data
        number_organizations_uzb = self.get_queryset().count()

        data = {
            'organizations': organizations,
            'number_organizations': number_organizations_uzb,
        }
        return Response(data, status=status.HTTP_200_OK)


class AboutPageView(MyListApiView):
    serializer_class = AboutPageSerializer
    queryset = models.Settings.objects.all()

    def get_object(self):
        return self.queryset.last()

    def get(self, request, *args, **kwargs):
        our_mission = self.get_serializer(self.get_object()).data
        number_volunteers = User.objects.filter(user_type=1).count()
        number_organizations = User.objects.filter(user_type=2).count()
        number_events = Event.objects.filter(status__in=[1, 2]).count()

        payload = {
            'our_mission': our_mission,
            'number_volunteers': number_volunteers,
            'number_organizations': number_organizations,
            'number_events': number_events
        }
        return Response(payload, status=status.HTTP_200_OK)
