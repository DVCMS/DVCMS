def is_student(user):
    return user.groups.filter(name='student').exists() or user.is_superuser


def is_lecturer(user):
    return user.groups.filter(name='lecturer').exists() or user.is_superuser
