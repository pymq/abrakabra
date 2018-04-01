from rest_framework import serializers, fields
from rest_framework.relations import Hyperlink
from .models import Ticket, Article
from django.contrib.auth.models import User
from rest_framework.reverse import reverse


class ArticleDetailHyperlink(serializers.HyperlinkedIdentityField):
    view_name = 'tickets-article-detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'parent_lookup_ticket': obj.ticket.id,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class ArticleHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    view_name = 'tickets-article-detail'

    def get_url(self, obj, view_name, request, format):
        if isinstance(obj, Ticket):
            return Hyperlink('', obj)

        kwargs = {
            'parent_lookup_ticket': obj.ticket.id,
            'pk': obj.id
        }
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class HyperlinkedTicketSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    articles = ArticleHyperlinkedRelatedField(view_name='tickets-article-detail', many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ('url', 'id', 'owner', 'title', 'created_at', 'state',
                  'type', 'priority', 'responsible', 'articles')
        read_only_fields = ('id', 'owner', 'created_at', 'articles')


class HyperlinkedArticleSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    url = ArticleDetailHyperlink(view_name='tickets-article-detail', read_only=True)
    ticket = serializers.HyperlinkedRelatedField(view_name='ticket-detail', read_only=True)

    class Meta:
        model = Article
        fields = ('url', 'id', 'owner', 'subject',
                  'created_at', 'message', 'ticket')
        read_only_fields = ('id', 'owner', 'created_at', 'ticket')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id', 'url')
