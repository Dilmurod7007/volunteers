import debug_toolbar
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.urls.conf import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from news.ckeditor_views import upload, browse

schema_view = get_schema_view(
    openapi.Info(
        title='UVA API',
        terms_of_services="",
        default_version='v1',
        contact=openapi.Contact(email="a@gnail.com"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('ckeditor/upload/', login_required(upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(browse)), name='ckeditor_browse'),
    path('admin/', admin.site.urls),
    re_path(r'^rosetta/', include('rosetta.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/v1/', include('config.api.urls')),
    path('', schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui", ),
    path('auth/', include('rest_framework.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

