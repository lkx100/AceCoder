from django.core.management import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print("Hello my Boy!!")