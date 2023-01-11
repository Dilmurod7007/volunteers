from django.urls import path

from . import views

app_name = 'event'

urlpatterns = [

    path('event/', views.EventsView.as_view(), name='event'),
    path('create-event', views.CreateEventView.as_view(), name='create-event'),
    path('event/<slug:slug>', views.EventDetailView.as_view(), name='event-detail'),
    path('like-event/<slug:slug>', views.LikeEventView.as_view(), name='like-event'),
    path('subscribe',  views.SubscribeView.as_view(), name='subscribe'),
    path('volunteers-of-event/<slug:slug>',  views.VolunteersOfEventView.as_view(), name='subscribe'),
    
]

