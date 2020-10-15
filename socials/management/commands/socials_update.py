from django.core.management.base import BaseCommand
# from django.utils.timezone import now

from socials.models import Configuration


class Command(BaseCommand):
    help = 'Get latest social posts'

    def handle(self, *args, **options):
        configuration = Configuration.objects.get_latest()
        configuration.refresh_token()
        configuration.refresh_media()
