from rest_framework import mixins, generics, status, viewsets
from django.contrib.auth.models import User
from .serializers import TicketSerializer, UserSerializer, ArticleSerializer, \
    CreateTicketSerializer
from .permissions import IsOwner
from rest_framework import permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route, api_view
from .models import Ticket, Article

from rest_framework_extensions.mixins import NestedViewSetMixin
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NestedArticleViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, ticket=Ticket.objects.get(pk=self.kwargs['parent_lookup_ticket']))


class NestedTicketViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('created_at', 'priority', 'title', 'type')
    ordering = ('-created_at',)
    filter_fields = ('priority', 'state', 'type', 'owner__username')

    def get_queryset(self):
        return self.request.user.tickets

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTicketSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, )
