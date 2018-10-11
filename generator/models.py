from __future__ import unicode_literals

from django.db import models
from django.core.cache import cache
from django.utils import timezone

from markovify.text import NewlineText
from markovify.chain import Chain

from generator import settings
from generator.utils import save_chain

from django_redis import get_redis_connection

import random

import datetime

import pickle


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


class Page(models.Model):
    """
    A randomly generated page
    """
    char_id = models.CharField(max_length=8, db_index=True)

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


class CharacterText(models.Model):
    """
    Character-dialog specific text
    """
    character_id = models.IntegerField(db_index=True)
    character = models.CharField(max_length=64,
                                 db_index=True)
    text = models.TextField()
    chain = models.TextField()

    markov = None

    def save(self, *args, **kwargs):
        # Generate the chain here
        super(CharacterText, self).save(*args, **kwargs)

    def generate_chain_file(self):
        """Generate a Markov chain file that can be loaded later"""
        self.markov = NewlineText(self.text)

        data = self.markov.chain.to_json()
        save_chain(self.character, data)

    def generate_sentence(self):
        """
        DEPRECATED
        Generate a sentence by loading Markov chain into memory
        """
        if self.markov is None:
            result = cache.get("character_text_pickle:%s" % self.character)

            if result is not None:
                self.markov = pickle.loads(result)
            else:
                self.markov = NewlineText(self.text)
                cache.set("character_text_pickle:%s" %
                          self.character, pickle.dumps(self.markov))

        # Try at most 10 times to generate a sentence
        for i in range(0, 10):
            title = self.markov.make_sentence()

            if title is not None:
                return title

        return None


class TitleText(models.Model):
    """
    Page title text
    """
    text = models.TextField()
    chain = models.TextField()

    markov = None

    def save(self, *args, **kwargs):
        # Generate the chain here
        super(TitleText, self).save(*args, **kwargs)


    def generate_chain_file(self):
        """Generate a Markov chain file that can be loaded later"""
        self.markov = NewlineText(self.text)

        data = self.markov.chain.to_json()
        save_chain("title", data)

    def generate_sentence(self):
        """
        DEPRECATED
        Generate a sentence by loading Markov chain into memory
        """
        if self.markov is None:
            result = cache.get("title_text_pickle")

            if result is not None:
                self.markov = pickle.loads(result)
            else:
                self.markov = NewlineText(self.text)
                cache.set("title_text_pickle", pickle.dumps(self.markov))

        # Try at most 10 times to generate a sentence
        for i in range(0, 10):
            title = self.markov.make_sentence()

            if title is not None:
                return title

        return None


class GeneralText(models.Model):
    """
    Text that doesn't fall under anything else
    """
    text = models.TextField()
    chain = models.TextField()

    markov = None

    def save(self, *args, **kwargs):
        # Generate the chain here
        super(GeneralText, self).save(*args, **kwargs)

    def generate_chain_file(self):
        """Generate a Markov chain file that can be loaded later"""
        self.markov = NewlineText(self.text)

        data = self.markov.chain.to_json()
        save_chain("general", data)

    def generate_sentence(self):
        """
        DEPRECATED
        Generate a sentence by loading Markov chain into memory
        """
        if self.markov is None:
            result = cache.get("general_text_pickle")

            if result is not None:
                self.markov = pickle.loads(result)
            else:
                self.markov = NewlineText(self.text)
                cache.set("general_text_pickle", pickle.dumps(self.markov))

        # Try at most 10 times to generate a sentence
        for i in range(0, 10):
            title = self.markov.make_sentence()

            if title is not None:
                return title

        return None
