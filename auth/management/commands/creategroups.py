from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create groups'

    def handle(self, *args, **options):
        groups = ['student', 'lecturer', 'admin']
        for group in groups:
            Group.objects.get_or_create(name=group)
            print(f"Created group {group}")

        # if alice does not exist
        if not User.objects.filter(username='alice').exists():
            User.objects.create_user(username='alice', password='alice2022')
            user = User.objects.get(username='alice')
            group = Group.objects.get(name='student')
            user.groups.add(group)
