from django.core.management.base import BaseCommand
# from django.utils.timezone import now

from socials.models import Configuration


class Command(BaseCommand):
    help = 'Get latest social posts'

    def handle(self, *args, **options):
        for configuration in Configuration.objects.all():
            if configuration.instagramconfiguration:
                child = configuration.instagramconfiguration
            if child:
                child.refresh()
