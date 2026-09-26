from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the core Student and Lecturer auth groups if they do not already exist."

    def handle(self, *args, **options):
        for group_name in ["Student", "Lecturer"]:
            _, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Group already exists: {group_name}"))
