from django.db.models import fields
from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from volunteer.models import User

from . import models


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Direction



class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['organization_name', 'email', 'phone', 'photo']
        model = User


class EventTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['word']
        model = models.Tag



class EventSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    direction = DirectionSerializer(read_only=True, many=True)
    tag = EventTagSerializer(read_only=True, many=True)
    oranization = UsersSerializer()
    active_volunteers = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'title', 'oranization', 'description', 'volunteers_needed',
         'active_volunteers','starting_date', 'finishing_date', 'slug',  
        'starting_time', 'finishing_time', 'contact_person', 'country', 'city', 'district', 'image', 
        'volunteers_will_be_paid', 'status', 'is_liked', 
         'tag', 'direction', 'created_date']
        model = models.Event

    def get_active_volunteers(self, event):
        active_volunteers = models.VolunteerForEvent.objects.filter(event=event, status=2).count()
        return active_volunteers


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Event



class CreateVolunteerForEventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['event']
        model = models.VolunteerForEvent



class VolunteerOfEventSerializer(serializers.ModelSerializer):
    event = StringRelatedField()
    volunteer = StringRelatedField()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        fields = ['event', 'volunteer', 'status']
        model = models.VolunteerForEvent



