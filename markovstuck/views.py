import json
import math

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django_redis import get_redis_connection
from generator.models import Leaderboards, Page
from ipware.ip import get_real_ip
from markovstuck.util import Paginator


def home(request):
    alltime_leaderboards = Leaderboards.get_all_time()
    last_month_leaderboards = Leaderboards.get_last_month()
    last_week_leaderboards = Leaderboards.get_last_week()
    last_day_leaderboards = Leaderboards.get_last_day()

    return render(
        request, "home/home.html",
        {"alltime_leaderboards": alltime_leaderboards,
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

    return render(
        request, "latest_entries/latest_entries.html",
        {"current_page": page,
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

    return render(
        request, "top_entries/top_entries.html", {
            "current_page": page,
            "entries": entries,
            "pages": pages,
            "total_pages": total_pages,
            "total_entry_count": total_entry_count})


def generate(request):
    page = Page.generate_page()

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

    return render(
        request, "view_page/view_page.html",
        {"page": page,
         "image_path": image_path,
         "voted": voted})
