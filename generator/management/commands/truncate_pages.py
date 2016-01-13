from django.core.management.base import BaseCommand
from django.utils import timezone

from generator.models import Page

class Command(BaseCommand):
    help = "Truncate non-saved pages that have existed for 24 hours"

    def handle(self, *args, **options):
        print("Truncating pages")

        old_datetime = timezone.now() - timezone.timedelta(hours=24)

        Page.objects.filter(datetime__lte=old_datetime,
                            saved=False).delete()

        print("Done!")
