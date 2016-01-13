from __future__ import absolute_import  # Python 2 only

import re
import types

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.forms.widgets import CheckboxInput
from django.core.cache import cache
from django_redis import get_redis_connection

from jinja2 import Environment
from jinja2.utils import contextfunction

from generator import settings

import random

from itertools import chain

"""
Various functions for the Jinja2 environment ported over from Django
"""
def get_path(context, url, arg):
    # If the singular argument was provided and starts with a forward
    # slash, use it as the path
    if arg is not None:
        if re.match('/', arg):
            return arg

    # Otherwise derive the path from the url tag approach
    return url

@contextfunction
def ancestor(context, url, arg=None):
    current_path = context['request'].path

    path = get_path(context, url, arg)
    
    # If the provided path is found at the root of the current path
    # render the contents of this tag
    if re.match(path, current_path):
        # Return either the contents of an ifancestor tag or the
        # ANCESTOR_PHRASE if it's an ancestor tag
        return 'active'
    
    return ''

def is_checkbox(field):
    return isinstance(field.field.widget, CheckboxInput)

def attr(field, args={}):
    # decorate field.as_widget method with updated attributes
    for attribute, value in args.items():
        old_as_widget = field.as_widget
    
    def process(widget, attrs, attribute, value):
        attrs[attribute] = value
    
    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html
    

    field.as_widget = types.MethodType(as_widget, field)
    return field
    
def join_by(value, arg):
    return arg.join(value)

def seconds_to_str(sec):
    sec = humanfriendly.format_timespan(sec)
    return sec

def pagination_list(current_page, entries_per_page, total_entries):
    entries = []
        
    total_pages = math.ceil(float(total_entries) / float(entries_per_page))
    
    # Add the first and previous pages
    if current_page != 1:
        entries.append("first")
        entries.append("previous")
    
    # Add four pages before the current page
    for i in range(0, 4):
        page = current_page - i
        
        if page >= 1:
            entries.append(page)
            
    # Add the current page
    entries.append(current_page)
    
    # Add four pages after the current page
    for i in range(0, 4):
        page = current_page + i
        
        if page <= total_pages:
            entries.append(page)
            
    # Add the next and last page
    if current_page != total_pages:
        entries.append("next")
        entries.append("last")
        
    return entries

def timesince_in_seconds(value):
    """
    Converts a provided datetime to amount of seconds that have passed
    """
    current_datetime = timezone.now()
    
    difference = current_datetime - value
    
    return difference.total_seconds()

def timeuntil_in_seconds(value):
    """
    Returns the time until a given datetime in seconds
    """
    current_datetime = timezone.now()
    
    difference = value - current_datetime
    
    return abs(difference.total_seconds())

def get_reversed_url(view_name, *args, **kwargs):
    """
    Works like the url tag in Django's own templating engine
    
    eg. {{ url('show_paste', arg1, kwarg1="arg") }}
    """
    return reverse(view_name, args=args, kwargs=kwargs)

def name_to_color(name):
    if name not in settings.NAME_COLORS:
        return "black"
    
    if type(settings.NAME_COLORS[name]) is list:
        return random.choice(settings.NAME_COLORS[name])
    else:
        return settings.NAME_COLORS[name]

JINJA_GLOBALS = {
    'ancestor': ancestor,
    'is_checkbox': is_checkbox,
    'attr': attr,
    'timesince_in_seconds': timesince_in_seconds,
    'timeuntil_in_seconds': timeuntil_in_seconds,
    'seconds_to_str': seconds_to_str,
    'pagination_list': pagination_list,
    'join_by': join_by,
    'url': get_reversed_url,
    'randint': random.randint,
    "name_to_color": name_to_color,
}