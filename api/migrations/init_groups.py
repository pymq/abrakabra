from __future__ import unicode_literals
from django.db import migrations


def forwards_func(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).bulk_create([
        Group(name="Agents"),
        Group(name="Customers"),
    ])


def reverse_func(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).filter(name="Agents").delete()
    Group.objects.using(db_alias).filter(name="Customers").delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
