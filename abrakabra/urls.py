from django.conf.urls import url, include
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import TemplateView

schema_view = get_schema_view(
    openapi.Info(
        title="Grishanya API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^', include('accounts.urls')),
    url(r'^api/', include('rest_auth.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^api/registration/', include('rest_auth.registration.urls')),
    url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('rest_framework.urls')),

]
