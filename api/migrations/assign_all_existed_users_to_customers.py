from __future__ import unicode_literals
from django.db import migrations


def forwards_func(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("auth", "User")
    db_alias = schema_editor.connection.alias
    users = User.objects.using(db_alias).all()
    group = Group.objects.using(db_alias).get(name='Customers')
    for user in users:
        user.groups.add(group)


def reverse_func(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("auth", "User")
    db_alias = schema_editor.connection.alias
    users = User.objects.using(db_alias).all()
    group = Group.objects.using(db_alias).get(name='Customers')
    for user in users:
        user.groups.remove(group)


class Migration(migrations.Migration):
    dependencies = [
        ('api', 'init_groups'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
