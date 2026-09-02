from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

User = get_user_model()


@receiver(m2m_changed, sender=User.groups.through)
def enforce_single_business_role(sender, instance, action, reverse, pk_set, **kwargs):
    if action != "pre_add" or not pk_set:
        return

    if reverse:
        for user in User.objects.filter(id__in=pk_set):
            existing_group_ids = set(
                user.groups.values_list("id", flat=True)
            )
            if existing_group_ids and instance.id not in existing_group_ids:
                raise ValidationError("A user can only belong to one group.")
        return

    existing_group_ids = set(
        instance.groups.values_list("id", flat=True)
    )

    if len(existing_group_ids | set(pk_set)) > 1:
        raise ValidationError("A user can only belong to one group.")
