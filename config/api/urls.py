from django.urls import path, include
from volunteer import views

app_name = 'volunteer'

urlpatterns = [
    path('', include('volunteer.urls')),
    path('', include('event.urls', namespace='event')),
    path('',include('news.urls', namespace="news")),
    path('',include('common.urls', namespace="common"))
]