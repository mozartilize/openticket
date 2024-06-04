from django.http import HttpRequest
from django.shortcuts import render, redirect

from openticket.models import Event
from openticket.lib import get_events_index, Paginator


def index(request: HttpRequest):
    return render(request, "index.html.j2")


def event_index(request: HttpRequest):
    events = get_events_index(Paginator(page=1, per_page=20))
    return render(request, "events/index.html.j2", context={"events": events})


def event_form(request: HttpRequest):
    if request.method == "POST":
        event = Event(
            name=request.POST["name"],
            number_of_tickets=request.POST["ticket_quantity"],
            start_date=request.POST["start"],
            end_date=request.POST["end"],
        )
        event.save()
        return redirect('event_index')

    return render(request, "events/new.html.j2")
