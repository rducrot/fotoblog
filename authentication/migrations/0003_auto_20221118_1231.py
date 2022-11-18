from django.core.management.sql import emit_post_migrate_signal

from django.db import migrations


def create_groups(apps, schema_migration):
    # ensure that permissions have been created
    emit_post_migrate_signal(verbosity=1, interactive=False, db='default')

    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    add_photo = Permission.objects.get(codename='add_photo')
    change_photo = Permission.objects.get(codename='change_photo')
    delete_photo = Permission.objects.get(codename='delete_photo')
    view_photo = Permission.objects.get(codename='view_photo')

    creator_permissions = [
        add_photo,
        change_photo,
        delete_photo,
        view_photo,
    ]

    creators = Group(name='creators')
    creators.save()
    creators.permissions.set(creator_permissions)

    subscribers = Group(name='subscribers')
    subscribers.save()
    subscribers.permissions.add(view_photo)

    for user in User.objects.all():
        if user.role == 'CREATOR':
            creators.user_set.add(user)
        if user.role == 'SUBSCRIBER':
            subscribers.user_set.add(user)


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20221118_0930'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
