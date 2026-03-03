
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from getpass import getpass

User = get_user_model()


#this create admin command is used to create an admin user for the application. 
# It prompts the user for a username and password, validates the input, and creates a new admin user if the input is valid. 
# The command also checks for existing usernames to prevent duplicates and ensures that the password meets certain criteria (e.g., minimum length).
class Command(BaseCommand):
    help = "Create an application admin user"

    def handle(self, *args, **kwargs):
        username = input("Admin username: ").strip()

        if not username:
            self.stdout.write(self.style.ERROR("Username cannot be empty"))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR("A user with this username already exists")
            )
            return

        password = getpass("Admin password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            self.stdout.write(self.style.ERROR("Passwords do not match"))
            return

        if len(password) < 8:
            self.stdout.write(
                self.style.ERROR("Password must be at least 8 characters long")
            )
            return

        user = User.objects.create_user(
            username=username,
            password=password,
            role="admin",
            is_staff=True,        # allows admin panel access
            is_superuser=True   # change to True if needed
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin user '{user.username}' created successfully"
            )
        )

