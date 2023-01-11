from django.urls import path

from news import pagination, serializers
from news.models import VideoMaterials

from . import views

app_name = 'news'

urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>', views.NewsDetailView.as_view(), name='news-detail'),
    path('school-of-volunteers', views.SchoolOfVolunteerView.as_view(), name='school-of-volunteer'),
    path('video-materials', views.VideoMaterialsView.as_view(), name='vide-materials'),
    path('video-materials/<slug:slug>', views.VideMaterialsDetailView.as_view(), name='vide-materials-detail'),
    path('materials', views.MaterialsView.as_view(), name='materials'),
    path('materials/<slug:slug>', views.MaterialsViewDetail.as_view(), name='materials-detail'),
    path('download-material/<slug:slug>', views.MaterialDownloadView.as_view(), name='download-material')

]
