from django.db.models import query
from django.http.response import FileResponse, HttpResponse
from rest_framework.response import Response

from news.pagination import MaterialPagination, NewsPagination, VideMaterialPagination
from django.views.decorators.http import require_http_methods
from wsgiref.util import FileWrapper
from django.shortcuts import get_object_or_404
from . import serializers
from rest_framework import generics, status
from news import models



class MyListApiView(generics.ListAPIView):

    # def get(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

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
       
       


class NewsListView(MyListApiView):
    serializer_class = serializers.NewsSerializer
    queryset = models.News.objects.all().order_by('-created_at')
    pagination_class = NewsPagination



class NewsDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.NewsSerializer
    queryset = models.News.objects.all()
    lookup_field = 'slug'

    def get(self, request, slug):
        new = get_object_or_404(models.News, slug=slug)

        news = serializers.NewsSerializer(new).data,
        other_news = serializers.NewsSerializer(models.News.objects.all().order_by('-created_at').exclude(slug=new.slug)[:4], many=True).data
        payload = {
            'news': news,
            'other_news': other_news
        }

        return Response(payload, status=status.HTTP_200_OK)



class SchoolOfVolunteerView(MyListApiView):
    queryset = models.VideoMaterials.objects.all()

    def get(self, request):
        video_materials = serializers.VideoMaterialSerializer(models.VideoMaterials.objects.all()[:6], many=True).data
        materials = serializers.MaterialsSerializer(models.Materials.objects.all()[:4], many=True).data

        payload = {
            'video_materials': video_materials,
            'materials': materials
        }

        return Response(payload)

    
class VideoMaterialsView(MyListApiView):
    queryset = models.VideoMaterials.objects.all().order_by('-created_at')
    serializer_class = serializers.VideoMaterialSerializer
    pagination_class = VideMaterialPagination


class VideMaterialsDetailView(generics.RetrieveAPIView):
    queryset = models.VideoMaterials.objects.all()
    serializer_class = serializers.VideoMaterialSerializer
    lookup_field = 'slug'

    def patch(self, request, slug):
        video_material = get_object_or_404(models.VideoMaterials, slug=slug)
        video_material.seen += 1
        video_material.save()
        return Response('+1 view.' + ' Overall = ' + str(video_material.seen) + ' views')


class MaterialsView(generics.ListAPIView):
    queryset = models.Material.objects.all().order_by('-created_at')
    serializer_class = serializers.MaterialsSerializer
    pagination_class = MaterialPagination


class MaterialsViewDetail(generics.RetrieveAPIView):
    queryset = models.Material.objects.all()
    serializer_class = serializers.MaterialsSerializer
    lookup_field = 'slug'

    def get(self, request, slug):
        context = {'request': request}
        material = get_object_or_404(models.Materials, slug=slug)
        similar_materials = models.Materials.objects.all().order_by('-created_at').exclude(slug=slug)

        payload = {
            'material': serializers.MaterialsSerializer(material).data,
            'similar_materials': serializers.MaterialsSerializer(similar_materials, many=True, context=context).data
        }

        return Response(payload, status=status.HTTP_200_OK)


class MaterialDownloadView(generics.ListAPIView):
    queryset = models.Material.objects.all()


    def get(self, request, slug, format=None):
        queryset = get_object_or_404(models.Material, slug=slug)
        file_handle = queryset.files.path
        document = open(file_handle, 'rb')
        queryset.downloaded += 1
        queryset.save()
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.files.name
        return response


