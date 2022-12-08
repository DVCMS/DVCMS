def is_student(user):
    return user.groups.filter(name='student').exists()


def is_lecturer(user):
    return user.groups.filter(name='lecturer').exists()