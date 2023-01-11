from django.urls import path

from . import views

app_name = 'common'

urlpatterns = [
    path('main_page/', views.MainPageView.as_view(), name='main_page_api'),
    # volunteers for map
    path('main_page_volunteers/', views.MainPageMapVolunteersListView.as_view(), name='main_page_volunteers'),
    # organizations for map
    path('main_page_organizations/', views.MainPageMapOrganizationsListView.as_view(), name='main_page_organizations'),
    path('common_part/', views.CommonPartListView.as_view(), name='common_part'),
    # about us page api
    path('about_us/', views.AboutPageView.as_view(), name='about_us')
]
