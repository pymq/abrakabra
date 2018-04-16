from rest_framework import serializers, fields
from .models import Ticket, Article
from django.contrib.auth.models import User


class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ticket
        fields = ('id', 'owner', 'title', 'created_at', 'state',
                  'type', 'priority', 'responsible')
        read_only_fields = ('id', 'owner', 'created_at')


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
        fields = ('title', 'state', 'type', 'priority',
                  'responsible', 'article')

    def create(self, validated_data):
        article_data = validated_data.pop('article')
        ticket = Ticket.objects.create(**validated_data)
        Article.objects.create(owner=validated_data.get('owner'), ticket=ticket,
                               **article_data)
        return ticket


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
