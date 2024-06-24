from typing import Optional, Any
from urllib.parse import urlencode

from django.urls import reverse
from django.http.response import HttpResponseRedirect


def redirect_to(
    viewname: str, *args: Any, query_params: Optional["dict[str, Any]"] = None, **kwargs: Any
):
    rev = reverse(viewname, *args, **kwargs)
    if query_params:
        rev = "{}?{}".format(rev, urlencode(query_params))
    return HttpResponseRedirect(rev)