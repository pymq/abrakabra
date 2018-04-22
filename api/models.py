from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('o', 'open'),
    ('c', 'closed'),
    ('r', 'reopen'),
)
TYPE_CHOICES = (
    ('common', 'common'),
    ('idk', 'I dont know'),
)
PRIORITY_CHOICES = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, default='o', max_length=40)
    type = models.CharField(choices=TYPE_CHOICES, default='common', max_length=40)  # TODO choices
    priority = models.CharField(choices=PRIORITY_CHOICES, default='0', max_length=2)
    owner = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    responsible = models.ForeignKey(User, related_name='tickets_responsible_for',
                                    on_delete=models.SET_NULL, null=True, default=None)  # TODO user groups

    def __str__(self):
        return self.title

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return request.user == self.owner or request.user.groups.filter(name="Agents")

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner or request.user.groups.filter(name="Agents")


class Article(models.Model):
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=4000)
    owner = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return self.owner == request.user or self.ticket.owner.id == request.user.id or \
               request.user.groups.filter(name="Agents")

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner
