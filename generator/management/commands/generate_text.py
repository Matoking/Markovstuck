from django.core.management.base import BaseCommand
from generator.models import GeneralText

class Command(BaseCommand):
    help = "Generate titles"

    def handle(self, *args, **options):
        general_text = GeneralText.objects.all()[0]

        for i in range(0, 25):
            print(general_text.generate_sentence())
