from django.urls import path

from event.views import EventDetailView
from . import views

from rest_framework.routers import DefaultRouter

app_name = 'volunteer'


urlpatterns = [
    path('user_email_code/', views.SendCodeToEmailAPIView.as_view(), name='user-email-code'),
    # email verification
    path('code_verification/', views.CodeVerification.as_view(), name='code-verification'),
    path('resend_code/', views.ReSendCodeAPIView.as_view(), name='resend-code'),
    # user register endpoints
    path('auth/register_volunteer/', views.VolunteerRegisterAPIView.as_view(), name='register-volunteer'),
    path('auth/register_organization/', views.OrganizationRegisterAPIView.as_view(), name='register-volunteer'),
    # login
    path('auth/login/', views.UserLoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutAPIView.as_view(), name='logout'),
    # volunteer profile update
    path('volunteer_profile/', views.VolunteerProfileUpdateView.as_view(), name='volunteer_profile_update'),
    # organization profile update
    path('organization_profile/', views.OrganizationProfileUpdateView.as_view(), name='organization_profile_update'),
    # password reset
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # volunteer events for profile
    path('volunteer_events/', views.VolunteerEventsView.as_view(), name='volunteer_events_list'),
    # organization events for profile
    path('organization_events/', views.OrganizationEventsView.as_view(), name='organization_events_list'),
    # organization events detail for profile
    path('organization_events/<int:pk>/', EventDetailView.as_view(), name='organization_event_detail'),
    # organization event volunteers
    path('organization_events/<int:pk>/volunteers/', views.EventVolunteersListView.as_view(), name='organization_event_volunteers'),
    # event volunteer info
    path('organization_events/<int:pk>/volunteers/<int:volunteer_id>/', views.EventVolunteerInfoView.as_view(),
         name='organization_event_volunteer_info'),
    # giving rating to volunteer
    path('giving_rating/<int:pk>/', views.GiveRatingView.as_view(), name='giving_rating_to_volunteer'),
    # volunteers list
    path('volunteers/', views.VolunteersList.as_view(), name='volunteers_list'),
    # volunteer detail
    path('volunteers/<int:pk>/', views.VolunteerDetailView.as_view(), name='volunteer_detail')
]
