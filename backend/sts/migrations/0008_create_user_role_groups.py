from django.db import migrations


ROLE_GROUP_NAMES = ("Developer", "QA", "Requester")


def create_role_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    for group_name in ROLE_GROUP_NAMES:
        Group.objects.get_or_create(name=group_name)


class Migration(migrations.Migration):
    dependencies = [
        ("sts", "0007_comment_comment_type"),
    ]

    operations = [
        migrations.RunPython(create_role_groups, migrations.RunPython.noop),
    ]
