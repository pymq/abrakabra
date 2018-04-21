from django.conf.urls import url, include
from django.views.generic import TemplateView

from accounts import views

urlpatterns = [
    url(r'^api/profile/$', views.current_user_info),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="accounts/password_reset_confirm.html"),
        name='password_reset_confirm'),

]
