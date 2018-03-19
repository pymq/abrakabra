from rest_framework import serializers
from .models import Ticket, Article
from django.contrib.auth.models import User


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Ticket
        fields = ('url', 'id', 'owner',
                  'title', 'created_at', 'state', 'type', 'priority', 'responsible')

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Article
        fields = ('url', 'id', 'owner',
                  'subject', 'created_at', 'message')




class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email')
