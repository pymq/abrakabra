from rest_framework import serializers
from .models import Ticket, Article


class TicketSerializerCustomers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ticket
        fields = ('id', 'owner', 'title', 'created_at', 'state',
                  'type', 'priority', 'responsible')
        read_only_fields = ('id', 'owner', 'created_at', 'type', 'priority', 'responsible')


class TicketSerializerAgents(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ticket
        fields = ('id', 'owner', 'title', 'created_at', 'state',
                  'type', 'priority', 'responsible')
        read_only_fields = ('id', 'owner', 'created_at', 'responsible')


class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    ticket = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'owner', 'subject',
                  'created_at', 'message', 'ticket')
        read_only_fields = ('id', 'owner', 'created_at', 'ticket')


class CreateTicketSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(write_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'state', 'type', 'priority',
                  'responsible', 'article')

    def create(self, validated_data):
        article_data = validated_data.pop('article')
        ticket = Ticket.objects.create(**validated_data)
        Article.objects.create(owner=validated_data.get('owner'), ticket=ticket,
                               **article_data)
        return ticket
