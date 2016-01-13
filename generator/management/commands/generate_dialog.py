from django.core.management.base import BaseCommand
from generator.models import CharacterText

class Command(BaseCommand):
    help = "Generate titles"

    def handle(self, *args, **options):
        character_text = CharacterText.objects.order_by("?").first()

        for i in range(0, 25):
            print("%s: %s" % (character_text.character,
                              character_text.generate_sentence()))
