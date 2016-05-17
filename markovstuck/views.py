from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.core.cache import cache

from generator.models import Leaderboards, ComicImage, Page, CharacterText, TitleText, GeneralText

from markovstuck.util import Paginator

from django_redis import get_redis_connection

from ipware.ip import get_real_ip

import random
import json
import string
import math


def home(request):
    alltime_leaderboards = Leaderboards.get_all_time()
    last_month_leaderboards = Leaderboards.get_last_month()
    last_week_leaderboards = Leaderboards.get_last_week()
    last_day_leaderboards = Leaderboards.get_last_day()

    return render(request, "home/home.html", {"alltime_leaderboards": alltime_leaderboards,
                                              "last_month_leaderboards": last_month_leaderboards,
                                              "last_week_leaderboards": last_week_leaderboards,
                                              "last_day_leaderboards": last_day_leaderboards})


def latest_entries(request, page=1):
    ENTRIES_PER_PAGE = 20

    page = int(page)

    total_entry_count = cache.get("total_entry_count")

    if total_entry_count is None:
        total_entry_count = Page.objects.filter(saved=True).count()
        cache.set("total_entry_count", total_entry_count)

    total_pages = math.ceil(float(total_entry_count) / float(ENTRIES_PER_PAGE))
    if page > total_pages:
        page = max(int(total_pages), 1)

    offset = (page - 1) * ENTRIES_PER_PAGE
    entries = cache.get("latest_entries:%s" % page)

    if entries is None:
        entries = Page.objects.filter(saved=True).order_by(
            "-datetime")[offset:(page * ENTRIES_PER_PAGE)]
        cache.set("latest_entries:%s" % page, entries, 15)

    pages = Paginator.get_pages(page, ENTRIES_PER_PAGE, total_entry_count)
    total_pages = int(
        math.ceil(float(total_entry_count) / float(ENTRIES_PER_PAGE)))

    return render(request, "latest_entries/latest_entries.html", {"current_page": page,
                                                                  "entries": entries,
                                                                  "pages": pages,
                                                                  "total_pages": total_pages,
                                                                  "total_entry_count": total_entry_count})

def top_entries(request, page=1):
    ENTRIES_PER_PAGE = 20

    page = int(page)

    total_entry_count = cache.get("total_entry_count")

    if total_entry_count is None:
        total_entry_count = Page.objects.filter(saved=True).count()
        cache.set("total_entry_count", total_entry_count)

    total_pages = math.ceil(float(total_entry_count) / float(ENTRIES_PER_PAGE))
    if page > total_pages:
        page = max(int(total_pages), 1)

    offset = (page - 1) * ENTRIES_PER_PAGE
    entries = cache.get("top_entries:%s" % page)

    if entries is None:
        entries = Page.objects.filter(saved=True).order_by(
            "-score")[offset:(page * ENTRIES_PER_PAGE)]
        cache.set("top_entries:%s" % page, entries, 15)

    pages = Paginator.get_pages(page, ENTRIES_PER_PAGE, total_entry_count)
    total_pages = int(
        math.ceil(float(total_entry_count) / float(ENTRIES_PER_PAGE)))

    return render(request, "top_entries/top_entries.html", {"current_page": page,
                                                            "entries": entries,
                                                            "pages": pages,
                                                            "total_pages": total_pages,
                                                            "total_entry_count": total_entry_count})


def generate(request):
    page = Page()

    # Generate title
    title_text = cache.get("title_text")

    if title_text is None:
        title_text = TitleText.objects.all()[0]
        cache.set("title_text", title_text)

    page.title = title_text.generate_sentence()

    # Get image
    page.image = ComicImage.get_random_image()

    general_text = cache.get("general_text")

    if general_text is None:
        general_text = GeneralText.objects.all()[0]
        cache.set("general_text", general_text)

    if random.randint(1, 10) >= 7:
        # Generate pre dialog text
        page.pre_dialog_text = general_text.generate_sentence()

    dialoglog = []

    if random.randint(1, 10) >= 5:
        # Generate dialoglog

        # How many characters will there be in the conversation
        characters_in_conv = random.randint(1, 3)
        conversation_length = random.randint(1, 4)

        character_count = CharacterText.objects.count()

        characters = []

        for i in range(0, characters_in_conv):
            random_char_id = random.randint(1, character_count)

            character = cache.get("character:%d" % random_char_id)

            if character is None:
                character = CharacterText.objects.get(
                    character_id=random_char_id)
                cache.set("character:%d" % random_char_id, character)

            characters.append(character)

        for i in range(0, conversation_length):
            # Pick a random character
            character = characters[random.randint(0, characters_in_conv - 1)]

            entry = {"char": character.character,
                     "logs": []}

            for j in range(0, random.randint(1, 3)):
                entry["logs"].append(character.generate_sentence())
            dialoglog.append(entry)

        page.dialoglog = json.dumps(dialoglog)

    if random.randint(1, 10) >= 6:
        # Generate post dialog text
        page.post_dialog_text = general_text.generate_sentence()

    page.char_id = ''.join(random.SystemRandom().choice(
        string.uppercase + string.lowercase + string.digits) for _ in xrange(8))

    # This is really unlikely (unless there's a problem with generating random numbers),
    # but check if the char ID already exists
    if Page.objects.filter(char_id=page.char_id).count() > 0:
        raise RuntimeError(
            "A duplicate char ID was generated. Consider participating in a lottery instead.")

    page.save()

    return redirect("view_page", char_id=page.char_id)


def vote(request, char_id):
    """
    Vote a page up
    """
    con = get_redis_connection("persistent")

    page = cache.get("page:%s" % char_id)

    if page is None:
        try:
            page = Page.objects.get(char_id=char_id)
            cache.set("page:%s" % char_id, page)
        except ObjectDoesNotExist:
            return render(request, "view_page/does_not_exist.html")
    elif not page:
        return render(request, "view_page/does_not_exist.html")

    # Has the user already voted
    ip = get_real_ip(request)

    if con.get("voted:%s:%s" % (ip, char_id)):
        # Visitor has already voted, just redirect him/her
        return redirect("view_page", char_id=char_id)
    else:
        page.score += 1
        page.saved = True
        page.save()
        con.setex("voted:%s:%s" % (ip, char_id), 86400, True)
        cache.set("page:%s" % char_id, page, 600)

    return redirect("view_page", char_id=char_id)


def view_page(request, char_id):
    con = get_redis_connection("persistent")

    page = cache.get("page:%s" % char_id)

    if page is None:
        try:
            page = Page.objects.get(char_id=char_id)
            cache.set("page:%s" % char_id, page, 600)
        except ObjectDoesNotExist:
            return render(request, "view_page/does_not_exist.html")
    elif not page:
        return render(request, "view_page/does_not_exist.html")

    page.dialoglog = json.loads(page.dialoglog)
    image_path = "../static/img/hs2/%s.gif" % page.image

    # Has the user voted
    ip = get_real_ip(request)
    voted = True if con.get("voted:%s:%s" % (ip, char_id)) else False

    return render(request, "view_page/view_page.html", {"page": page,
                                                        "image_path": image_path,
                                                        "voted": voted})
