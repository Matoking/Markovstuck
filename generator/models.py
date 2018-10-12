from django.db import models
from django.core.cache import cache
from django.utils import timezone

from django_redis import get_redis_connection

import random
import requests

import json
import string


class Leaderboards(object):
    """
    Get page leaderboards
    """
    @staticmethod
    def get_all_time():
        pages = cache.get("alltime_leaderboards")

        if pages is None:
            pages = Page.objects.filter(saved=True).order_by(
                "-score").only("title", "char_id", "score", "datetime")[0:10].values()
            cache.set("alltime_leaderboards", pages, 300)

        return pages

    @staticmethod
    def get_last_month():
        pages = cache.get("last_month_leaderboards")

        if pages is None:
            month_ago = timezone.now() - timezone.timedelta(days=30)
            pages = Page.objects.filter(saved=True,
                                        datetime__gte=month_ago).order_by("-score").only("title", "char_id", "score", "datetime")[0:10].values()
            cache.set("last_month_leaderboards", pages, 300)

        return pages

    @staticmethod
    def get_last_week():
        pages = cache.get("last_week_leaderboards")

        if pages is None:
            week_ago = timezone.now() - timezone.timedelta(days=7)
            pages = Page.objects.filter(saved=True,
                                        datetime__gte=week_ago).order_by("-score").only("title", "char_id", "score", "datetime")[0:10].values()
            cache.set("last_week_leaderboards", pages, 300)

        return pages

    @staticmethod
    def get_last_day():
        pages = cache.get("last_day_leaderboards")

        if pages is None:
            day_ago = timezone.now() - timezone.timedelta(hours=24)
            pages = Page.objects.filter(saved=True,
                                        datetime__gte=day_ago).order_by("-score").only("title", "char_id", "score", "datetime")[0:10].values()
            cache.set("last_day_leaderboards", pages, 60)

        return pages


class ComicImage(object):
    """
    Get a random image from the comic
    """
    @staticmethod
    def get_random_image():
        con = get_redis_connection("persistent")

        image_no = con.srandmember("panel_images")

        if image_no is None:
            raise Exception("No image found! Are you sure you've configured Redis correctly and run 'update_images' command?")

        image_file_no = "%d" % int(image_no)

        chars_to_add = 5 - len(image_file_no)

        for i in range(0, chars_to_add):
            image_file_no = "0%s" % image_file_no

        return image_file_no


# Character names corresponding to Markov chains that exist for each character
CHARACTER_NAMES = [
    'SOLLUX', 'PAA', 'PTA', 'PAG', 'CCG', 'CCC', 'NEPETA', 'FGA', 'TEREZI',
    'GT', 'GG', 'GC', 'GA', 'FAC', 'DIRK', 'ARADIABOT', 'ROSE', 'ARQUIUSPRITE',
    'FAG', 'uu', 'EQUIUS', 'ARADIASPRITE', 'ROXY', 'AC', 'PCG3', 'MEENAH',
    'JAKE', 'GAMZEE', 'PCA', 'PCG', 'CEB', 'JASPROSESPRITE^2', 'FCG2', 'PTC',
    'VRISKA', 'KANAYA?', 'EB', 'KARKAT', 'FTC', 'UU', 'KANAYA',
    'DAVEPETASPRITE^2', 'ARADIA', '?CG', 'JADE', 'DAVE', 'CTG', 'CTA',
    'ARANEA', 'FCT', 'CGC', 'FCA', 'FCG', 'FGC', 'JOHN', 'TAVROS', 'CC',
    'CA', 'CG', 'ROSESPRITE', 'CT', 'PCG8', 'PCG6', 'PCG7', 'PCG4', 'PCG5',
    'PCG2', 'FEFERI', 'CALLIOPE', 'DAVESPRITE', '?TG', 'PCC', 'CAC', 'CAA',
    'CAG', 'PGC', 'TT', 'TG', 'FAA', 'TC', 'TA', 'AA', 'AG', 'AT', 'ERIDAN',
    'TAVROSPRITE', 'JANE'
]


class Page(models.Model):
    """
    A randomly generated page
    """
    char_id = models.CharField(max_length=8, db_index=True, unique=True)

    title = models.TextField()

    image = models.TextField()

    # Any text before the dialoglog (if any)
    pre_dialog_text = models.TextField(default="")

    # Any dialoglog entries (if any)
    dialoglog = models.TextField(default="[]")

    # Any text after the dialoglog (if any)
    post_dialog_text = models.TextField(default="")

    # When generated
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)

    # Has this page been saved
    # If not, it will automatically be deleted after a short while (about 24
    # hours)
    saved = models.BooleanField(default=False)
    score = models.IntegerField(default=0, db_index=True)

    @staticmethod
    def generate_page():
        """
        Generate a random page
        """
        page = Page()

        # Get image
        page.image = ComicImage.get_random_image()

        json_request = {}

        if random.randint(1, 10) >= 7:
            # Generate pre dialog text
            json_request["generate_pre_dialog"] = True

        json_request["characters"] = []

        if random.randint(1, 10) >= 5:
            # How many characters will there be in the conversation
            characters_in_conv = random.randint(1, 3)
            json_request["conversation_length"] = random.randint(1, 4)

            json_request["characters"] = random.sample(
                CHARACTER_NAMES, characters_in_conv
            )

        json_request["characters"] = json.dumps(json_request["characters"])

        if random.randint(1, 10) >= 6:
            # Generate post dialog text
            json_request["generate_post_dialog"] = True

        response = requests.post("http://127.0.0.1:5666/", data=json_request)
        response = json.loads(response.text)

        page.char_id = ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(8)
        )

        page.title = response["title"]

        if "dialoglog" in response:
            page.dialoglog = json.dumps(response["dialoglog"])

        if "pre_dialog_text" in response:
            page.pre_dialog_text = response["pre_dialog_text"]

        if "post_dialog_text" in response:
            page.post_dialog_text = response["post_dialog_text"]

        page.save()

        return page
