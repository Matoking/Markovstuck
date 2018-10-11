import os
from urllib.error import HTTPError

import wget
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django_redis import get_redis_connection
from generator import settings
from generator.models import CharacterText, GeneralText


class Command(BaseCommand):
    help = "Update the images"

    def add_arguments(self, parser):
        parser.add_argument("--reset", dest="reset", action="store_true",
                            help="If true, clear the list of images and download all of them again")

    def handle(self, *args, **options):
        """
        Download and update the list of images to use
        """
        con = get_redis_connection("persistent")

        start = settings.IMAGE_START

        if options["reset"]:
            con.delete("panel_images")
            print("Image list reset, everything will be downloaded again now.")

        # Get the current list if it exists
        images = con.smembers("panel_images")

        # Create the directory for images if it doesn't exist
        if not os.path.isdir(settings.IMAGE_PATH):
            os.makedirs(settings.IMAGE_PATH)

        if len(images) > 0:
            # If the last update attempt was unfinished, start from
            # where we left off
            for image_no in images:
                image_no = int(image_no)
                if image_no > start:
                    start = image_no + 1

        print("Downloading images starting from %d to %d" %
              (start, settings.IMAGE_END))

        for i in range(start, settings.IMAGE_END + 1):
            image_file_no = "%d" % i
            chars_to_add = 5 - len(image_file_no)

            for j in range(0, chars_to_add):
                image_file_no = "0%s" % image_file_no

            image_path = "%s/%s.gif" % (settings.IMAGE_PATH, image_file_no)

            try:
                wget.download("https://www.homestuck.com/images/storyfiles/hs2/%s.gif" % image_file_no,
                              image_path)
            except HTTPError as exc:
                if exc.code == 404:
                    print("Image #%d doesn't exist, skipped" % i)
                    continue
                else:
                    raise

            con.sadd("panel_images", i)
            print("\nImage #%d added" % i)

        print("Done!")
