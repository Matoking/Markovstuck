from django.core.management.base import BaseCommand
from generator.models import TitleText

class Command(BaseCommand):
    help = "Generate titles"

    def handle(self, *args, **options):
        title_text = TitleText.objects.all()[0]

        for i in range(0, 25):
            print(title_text.generate_sentence())
