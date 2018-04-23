from rest_framework import mixins, generics, status, viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from . import serializers
from .models import Ticket, Article

from rest_framework_extensions.mixins import NestedViewSetMixin

from django_filters.rest_framework import DjangoFilterBackend

from dry_rest_permissions.generics import DRYPermissions


class NestedArticleViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, DRYPermissions,)

    def get_queryset(self):
        queryset = None
        if self.request.user.groups.filter(name="Agents"):
            queryset = Article.objects.all()
        if self.request.user.groups.filter(name="Customers"):
            queryset = Article.objects.filter(ticket__owner=self.request.user)
        return self.filter_queryset_by_parents_lookups(queryset)

    def create(self, request, *args, **kwargs):
        if Ticket.objects.get(pk=self.kwargs['parent_lookup_ticket']).owner != request.user and \
                self.request.user.groups.filter(name="Customers"):
            raise PermissionDenied()
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, ticket=Ticket.objects.get(pk=self.kwargs['parent_lookup_ticket']))


class NestedTicketViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, DRYPermissions,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('created_at', 'priority', 'title', 'type')
    ordering = ('-created_at',)
    filter_fields = ('priority', 'state', 'type', 'owner__username')

    def get_queryset(self):
        if self.request.user.groups.filter(name="Agents"):
            return Ticket.objects.all()
        if self.request.user.groups.filter(name="Customers"):
            return self.request.user.tickets

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateTicketSerializer
        if self.request.user.groups.filter(name="Agents"):
            return serializers.TicketSerializerAgents
        if self.request.user.groups.filter(name="Customers"):
            return serializers.TicketSerializerCustomers
        # return serializers.TicketSerializerCustomers

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, )
