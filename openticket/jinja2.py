import os
import json

from django.conf import settings
from django.urls import reverse
from django.templatetags.static import static
from jinja2 import Environment


def environment(**options):
    # TODO: only work for local development by now
    static_dir = settings.STATICFILES_DIRS[0]
    with open(os.path.join(static_dir, 'meta.json')) as f:
        static_hash = json.load(f)['hash']
    env = Environment(**options)
    env.globals.update({"static": static, "url": reverse, "static_hash": static_hash})
    return env