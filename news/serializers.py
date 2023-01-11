from django.db.models import fields
from rest_framework import serializers
from . import models


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = ('id', 'title', 'body', 'posted_date', 'photo')


class VideoMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoMaterials
        fields = ('id', 'title', 'video', 'seen', 'slug', 'created_at', )
        

class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = ('id', 'title', 'files', 'body', 'image', 'slug', 'downloaded')



