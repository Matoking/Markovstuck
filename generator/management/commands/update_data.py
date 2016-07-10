from django.core.management.base import BaseCommand

import requests
import re

from sets import Set

from bs4 import BeautifulSoup

from generator import settings
from generator.models import CharacterText, TitleText, GeneralText

class Command(BaseCommand):
    help = "Update the models and other data"

    # Page titles
    titles = []

    # Other text
    text = []

    # Character dialog
    dialog = {}

    aliases = {}

    names = Set()

    def handle(self, *args, **options):
        print("Loading pages")

        self.create_aliases()

        for url in settings.URLS:
            data = requests.get(url)

            if data.status_code == 200:
                print("Loaded page %s" % url)
                self.handle_html(data.text)
            else:
                print("Couldn't fetch url %s" % url)

        print("Saving text")

        self.save_text()

        print("Done!")

    def handle_html(self, html):
        """
        Handle the HTML data we fetched
        """
        soup = BeautifulSoup(html, 'lxml')
        print("Parsed page")

        text = soup.find("table", width="80%").find("td").contents[1].text
        lines = text.split("\n")

        for line in lines:
            # Ignore empty lines
            if line.strip() == "":
                continue

            # Check if it starts a pesterlog
            if line.strip() in settings.IGNORE_LINES:
                continue

            # Check if it contains a title
            match = re.search("\ ([0-9]{2})\/([0-9]{2})\/([0-9]{2})", line)

            if match is not None:
                # It's a title
                self.titles.append(line[13:len(line)-1])
                continue

            # Check if it's dialog
            if line.find(":", 0, 25):
                name = line[0:line.find(":")]
                dialog_text = line[line.find(":")+1:]

                if name not in settings.NAMES and len(name) <= 3 and name.isupper():
                    self.names.add(name)
                    continue

                if name in settings.NAMES:
                    if name not in self.dialog:
                        self.dialog[name] = [dialog_text]
                    else:
                        self.dialog[name].append(dialog_text)

                    # Add dialog also to the aliases
                    if name in self.aliases:
                        for alias in self.aliases[name]:
                            if alias not in self.dialog:
                                self.dialog[alias] = [dialog_text]
                            else:
                                self.dialog[alias].append(dialog_text)
                    continue

            # Otherwise it's probably just normal text
            self.text.append(line)

    def create_aliases(self):
        for aliases in settings.NAME_ALIASES:
            for i, name in enumerate(aliases):
                aliases_copy = list(aliases)
                aliases_copy.pop(i)
                self.aliases[name] = aliases_copy

    def save_text(self):
        """
        Save all the text we just loaded and parsed
        """
        # Clear all previous entries
        TitleText.objects.all().delete()
        CharacterText.objects.all().delete()
        GeneralText.objects.all().delete()

        # Save all the models
        title_text = TitleText(text="\n".join(self.titles))
        title_text.save()
        title_text.generate_chain_file()

        character_id = 1

        for character, text in self.dialog.items():
            # Skip characters that don't have enough material to work with
            if len(text) < 200:
                continue

            character_text = CharacterText(character_id=character_id,
                                           character=character,
                                           text="\n".join(self.dialog[character]))
            character_text.save()
            character_text.generate_chain_file()
            character_id += 1

        general_text = GeneralText(text="\n".join(self.text))
        general_text.save()
        general_text.generate_chain_file()
