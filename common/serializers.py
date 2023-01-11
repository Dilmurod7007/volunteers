from rest_framework import serializers
from common import models
from common.models import Slider, Menu, Partner, SocialNetwork, Settings
from event.models import Event, Tag
from volunteer.models import User, Region, District, VolunteerRating


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('text', 'additional_link', 'facebook', 'instagram', 'telegram', 'youtube')


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('phone', 'facebook', 'instagram', 'telegram', 'youtube', 'additional_link')


class VolunteerProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'photo', 'user_type')


class OrganizationProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'organization_name', 'photo', 'user_type')


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('facebook', 'telegram', 'instagram')


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ('id', 'name', 'logo', 'link', 'order', 'is_active')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('title', 'link', 'is_right', 'order', 'slug', 'is_active')


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ('title', 'text', 'active', 'order', 'link', 'photo')


class MainPageSerializer(serializers.Serializer):
    pass


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('word', 'slug')


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_type', 'organization_name', 'photo')


class UserEventSerializer(serializers.ModelSerializer):
    oranization = OrganizationSerializer()
    tag = TagSerializer(many=True)
    city = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')
    district = serializers.SlugRelatedField(queryset=District.objects.all(), slug_field='name')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'starting_date', 'finishing_date', 'starting_time',
                  'finishing_time', 'image', 'city', 'district', 'status', 'is_liked', 'tag', 'rating', 'oranization')

    def get_rating(self, obj):
        try:
            volunteer_rating_instance = VolunteerRating.objects.get(volunteer=self.context.get('request').user,
                                                                    organization=obj.oranization)
        except VolunteerRating.DoesNotExist:
            return None
        return volunteer_rating_instance.rating


class VolunteerLikedEventSerializer(serializers.ModelSerializer):
    oranization = OrganizationSerializer()
    tag = TagSerializer(many=True)
    city = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')
    district = serializers.SlugRelatedField(queryset=District.objects.all(), slug_field='name')

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'starting_date', 'finishing_date', 'starting_time',
                  'finishing_time', 'image', 'city', 'district', 'tag', 'oranization')


class CommonPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('phone', 'text', 'aphorism', 'additional_link')


class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('our_mission',)
