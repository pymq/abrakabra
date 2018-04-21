from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse

from accounts import serializers


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=(permissions.IsAuthenticated,))
def current_user_info(request):
    """
    Возвращает информацию о текущем пользователе
    """
    user = request.user
    serializer = serializers.UserSerializer(user)
    return JsonResponse(serializer.data, safe=False)
