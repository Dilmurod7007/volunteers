from datetime import datetime

from django.db.models import Count, Avg
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from .models import User, Country, Region, District, UserEmailCode, VolunteerRating, UserProfile, \
    Language, Goal


class EmailInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class RegionSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', queryset=Country.objects.all())

    class Meta:
        model = Region
        fields = ('id', 'name', 'country')


class DistrictSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(slug_field='name', queryset=Region.objects.all())

    class Meta:
        model = District
        fields = ('id', 'name', 'region')


class UserEmailCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmailCode
        fields = ('id', 'email', 'code', 'date_created')


class VolunteerRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=32, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'date_of_birth',
                  'country', 'region', 'district', 'phone', 'photo', 'password', 'password2')

    def create(self, validated_data):
        password = validated_data.get('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError(_('Parollar mos kelmadi, Iltimos qayta urinib ko\'ring!!!'))
        else:
            user = super(VolunteerRegisterSerializer, self).create(validated_data)
            user.set_password(password)
            user.is_active = True
            user.user_type = 1
            user.save()
            UserProfile.objects.create(user=user)
            return user


class OrganizationRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=32, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'organization_type', 'organization_name', 'person_for_contact',
                  'country', 'region', 'district', 'phone', 'photo', 'about', 'password', 'password2')

    def create(self, validated_data):
        password = validated_data.get('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError(_('Parollar mos kelmadi, Iltimos qayta urinib ko\'ring!!!'))
        else:
            user = super(OrganizationRegisterSerializer, self).create(validated_data)
            user.set_password(password)
            user.is_active = True
            user.user_type = 2
            user.save()
            UserProfile.objects.create(user=user)
            return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class MainPageOrganizationSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'organization_name', 'photo', 'region', 'phone', 'about', 'facebook', 'instagram')


class OrganizationForMapSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'organization_name', 'photo', 'email', 'region')


class MainPageVolunteerSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='name')
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo', 'country', 'region')


class VolunteerForMapSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo', 'region', 'district', 'phone', 'age', 'rating')

    def get_rating(self, obj):
        rating = VolunteerRating.objects.filter(volunteer=obj).aggregate(avg_rating=Avg('rating'))
        return rating

    def get_age(self, obj):
        age = datetime.now().year - obj.date_of_birth.year
        return age


class VolunteerProfileSerializer(serializers.ModelSerializer):
    languages = serializers.SlugRelatedField(queryset=Language.objects.all(), slug_field='name', many=True)
    goals = serializers.SlugRelatedField(queryset=Goal.objects.all(), slug_field='name', many=True)

    class Meta:
        model = UserProfile
        fields = ('about_me', 'education_level', 'specialty', 'languages', 'interests', 'goals')


class VolunteerProfileUpdateSerializer(serializers.ModelSerializer):
    profile = VolunteerProfileSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'rating', 'photo', 'profile')

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        languages = profile.pop('languages', None)
        goals = profile.pop('goals', None)
        user_profile = UserProfile.objects.get(user=instance)
        user_profile.user = instance
        user_profile.languages.clear()
        user_profile.goals.clear()
        if languages is not None:
            for language in languages:
                user_profile.languages.add(language)
        if goals is not None:
            for goal in goals:
                user_profile.goals.add(goal)
        user_profile.save()
        UserProfile.objects.update(**profile)
        return super(VolunteerProfileUpdateSerializer, self).update(instance, validated_data)

    def get_rating(self, obj):
        rating = VolunteerRating.objects.filter(volunteer=obj).aggregate(rating=Avg('rating'))
        return rating


class OrganizationProfileUpdateSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='name')
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')
    district = serializers.SlugRelatedField(queryset=District.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'organization_name', 'person_for_contact', 'photo', 'country', 'region', 'district',
                  'phone', 'email', 'facebook', 'telegram', 'instagram', 'youtube', 'about')


class UserPasswordResetSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=32, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(max_length=32, style={'input_type': 'password'}, write_only=True)
    new_password2 = serializers.CharField(max_length=32, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2')

    def update(self, instance, validated_data):
        old_password = validated_data.get('old_password')
        new_password = validated_data.get('new_password')
        new_password2 = validated_data.get('new_password2')
        if instance.check_password(old_password):
            if new_password == new_password2:
                instance.set_password(new_password)
            else:
                raise ValidationError(_('Yangi kiritilgan parollar mmos kelmadi'))
        else:
            raise ValidationError(_("Siz noto'g'ri parol kiritdingiz"))
        instance.save()
        return instance


class EventVolunteersSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo', 'region', 'district', 'phone', 'age')

    def get_age(self, obj):
        age = datetime.now().year - obj.date_of_birth.year
        return age


class GiveRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerRating
        fields = ('volunteer', 'organization', 'rating')


class VolunteerInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    age = serializers.SerializerMethodField()
    date_of_birth = serializers.DateField()
    avg_rating = serializers.FloatField()
    profile = VolunteerProfileSerializer()
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')
    district = serializers.SlugRelatedField(queryset=District.objects.all(), slug_field='name')
    facebook = serializers.URLField()
    instagram = serializers.URLField()
    telegram = serializers.URLField()
    youtube = serializers.URLField()

    def get_age(self, obj):
        age = datetime.now().year - obj.date_of_birth.year
        return age
#
# class VolunteerDetailSerializer(serializers.ModelSerializer):
#     class Meta:

