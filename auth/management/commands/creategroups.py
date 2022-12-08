from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create groups'

    def handle(self, *args, **options):
        groups = ['student', 'lecturer']
        for group in groups:
            Group.objects.get_or_create(name=group)
            print(f"Created group {group}")
