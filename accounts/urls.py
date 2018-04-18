from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="accounts/password_reset_confirm.html"),
        name='password_reset_confirm'),

]
