from django.conf.urls import url, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from rest_framework_extensions.routers import ExtendedSimpleRouter, NestedRouterMixin

schema_view = get_schema_view(title='Grishanya API')

router = DefaultRouter()
router.register(r'users', views.UserViewSet)


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


nested_router = NestedDefaultRouter()
(nested_router.register(r'tickets', views.NestedTicketViewSet, base_name='ticket')
 .register(r'articles',
           views.NestedArticleViewSet,
           base_name='tickets-article',
           parents_query_lookups=['ticket'])
 )

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(nested_router.urls)),
    url(r'^schema/$', schema_view),
    url(r'^api/', include('rest_framework.urls')),
]
