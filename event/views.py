from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from . import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.cache import _generate_cache_header_key
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from .models import Event, VolunteerForEvent, VolunteerStatus
from . import filters


class MyListApiView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class MyDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyDetailViewCountAPIView(generics.RetrieveAPIView):
    def get_object(self):
        object = super().get_object()
        cache_key = _generate_cache_header_key('views_count', self.request)
        if not cache.get(cache_key):
            object.views = object.views + 1
            object.save(update_fields=['views'])
            cache.set(cache_key, '1', settings.VIEW_COUNT_PERIOD)
        return object


class MyDestroyApiView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyUpdateApiView(generics.UpdateAPIView):
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, context=request, partial=True)
        if not serializer.is_valid(raise_exception=False):
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.updated_at = timezone.now()
        instance.updated_by = request.user
        partial = kwargs.pop('partial', False)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


def check_liked_and_check_status(user, events):
    for event in events:
            if event.finishing_date < date.today():
                event.status = Event.EventStatus.finished
                event.save()
          
            # is_event = Event.objects.get(id=event.id, liked_user__id__in=str(user.id))
            is_event = get_object_or_404(Event, id=event.id, liked_user__id__in=str(user.id))
            if is_event:
                event.is_liked = True
                event.save()
            else:
                event.is_liked = False
                event.save()



class EventsView(generics.ListAPIView):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = filters.EventFilter

    def get(self, request):
        context = {'request': request}
        events = Event.objects.all()
        check_liked_and_check_status(request.user, events)
        serializer = serializers.EventSerializer(self.filter_queryset(events), many=True, context=context)
        return Response(serializer.data)


class EventDetailView(generics.DestroyAPIView):
    queryset = models.Event.objects.all()
    lookup_field = "slug"

    def get(self, request, slug):
        context = {'request': request}
        event_excluded = Event.objects.all().exclude(slug=slug)

        #searching 3 similar events
        similar_events_tuple = ()
        direction_id_list = Event.objects.filter(slug=slug).values_list('direction__id', flat=True)
        filter_by_status = event_excluded.filter(status=3)
        similar_events_tuple += tuple(filter_by_status.values_list('id', flat=True))
        if filter_by_status.count() < 3:
            filter_by_direction = event_excluded.filter(direction__id__in = tuple(direction_id_list)).exclude(id__in=tuple(similar_events_tuple))
            similar_events_tuple += tuple(filter_by_direction.values_list('id', flat=True))
            if (filter_by_direction.count() + filter_by_status.count()) < 3:
                other_events = event_excluded.all().exclude(id__in=tuple(similar_events_tuple))
                similar_events_tuple += tuple(other_events.values_list('id', flat=True))

        event = Event.objects.filter(slug=slug)
        similar_event = Event.objects.filter(id__in=tuple(similar_events_tuple))
        check_liked_and_check_status(request.user, similar_event)
        check_liked_and_check_status(request.user, event)

        event = serializers.EventSerializer(event, many=True, context=context).data
        similar_events = serializers.EventSerializer(similar_event, many=True, context=context).data
        payload = {
            'event': event,
            'similar_events': similar_events
        }
        return Response(payload, status=status.HTTP_200_OK)



class CreateEventView(generics.CreateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.CreateEventSerializer
    permission_classes = [permissions.IsAuthenticated]



class SubscribeView(generics.CreateAPIView):
    serializer_class = serializers.CreateVolunteerForEventSerializer
    queryset = models.VolunteerForEvent.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        event = get_object_or_404(Event, id=request.data['event'])
        volunteer_for_event = VolunteerForEvent.objects.filter(volunteer=request.user, event=event).first()
        if request.user.get_user_type_display() == 'Volontyor':
            if volunteer_for_event:
                if volunteer_for_event.status == VolunteerStatus.canceled:
                    volunteer_for_event.status = VolunteerStatus.registered
                    volunteer_for_event.save()
                    return Response("Volunteers status changed to 'REGISTERED'")
                else:
                    volunteer_for_event.status = VolunteerStatus.canceled
                    volunteer_for_event.save()
                    return Response("Volunteers status changed to 'CANCELED'")

            else:
                VolunteerForEvent.objects.create(event=event, volunteer=request.user)
                return Response('New volunteer succesfully added')
        else:       
            return Response('User is not volunteer')


class VolunteersOfEventView(generics.ListAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    
    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        volunteers = models.VolunteerForEvent.objects.filter(event=event)
        serializer = serializers.VolunteerOfEventSerializer(volunteers, many=True)
        return Response(serializer.data)



class LikeEventView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def patch(self, request, slug):
        event  = get_object_or_404(Event, slug=slug)
        if Event.objects.filter(liked_user__id__in = str(request.user.id), slug=slug).exists():
            event.liked_user.remove(request.user)
            return Response('Succesfully Disliked')
        else:
            event.liked_user.add(request.user)
            return Response('Succesfully Liked')





