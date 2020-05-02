from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create admin command'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str)
        parser.add_argument('-e', '--email', type=str)
        parser.add_argument('-p', '--password', type=str)

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                username,
                email,
                password,
            )
            self.stdout.write('Admin user has created')
        else:
            self.stdout.write('Admin user with provided credentials exists')
