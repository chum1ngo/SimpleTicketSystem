from django.db import models


class UserRole(models.TextChoices):
    DEVELOPER = "DEVELOPER", "Developer"
    QA = "QA", "QA"
    REQUESTER = "REQUESTER", "Requester"


GROUP_ROLE_MAP = {
    "Developer": UserRole.DEVELOPER,
    "QA": UserRole.QA,
    "Requester": UserRole.REQUESTER,
}


def get_user_role(user):
    group_names = set(
        user.groups.values_list("name", flat=True)
    )

    for group_name, role in GROUP_ROLE_MAP.items():
        if group_name in group_names:
            return role

    return UserRole.REQUESTER
