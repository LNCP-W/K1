from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from config import settings


class Command(BaseCommand):
    help = "Creates a superuser if one does not exist"

    def handle(self, *args, **options):
        """
        Checks if a superuser already exists. If not, creates one with credentials from settings.

        Args:
            *args: Positional arguments passed to the command (not used in this case).
            **options: Keyword arguments passed to the command (not used in this case).

        Creates:
            A superuser with the username, email, and password provided in the settings.

        Logs:
            - Success message if the superuser is created or already exists.
        """
        User = get_user_model()
        username = settings.superuser.username
        email = settings.superuser.email
        password = settings.superuser.password

        # Check if superuser exists
        if not User.objects.filter(username=username).exists():
            # Create superuser if it does not exist
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" already exists.')
            )
