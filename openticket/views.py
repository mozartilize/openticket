from django.http import HttpRequest
from django.shortcuts import render, redirect

from openticket.models import Event
from openticket.lib import get_events_index, EventsFilter, EventsFilterInput


def index(request: HttpRequest):
    return render(request, "index.html.j2")


def event_index(request: HttpRequest):
    events_filter = EventsFilter(data=request.GET, initial=request.GET)
    events_filter.is_valid()
    events = get_events_index(
        EventsFilterInput(**events_filter.cleaned_data)
    )
    return render(
        request,
        "events/index.html.j2",
        context={"events": events, "events_filter": events_filter},
    )


def event_form(request: HttpRequest):
    if request.method == "POST":
        event = Event(
            name=request.POST["name"],
            number_of_tickets=request.POST["ticket_quantity"],
            start_date=request.POST["start"],
            end_date=request.POST["end"],
        )
        event.save()
        return redirect("event_index")

    return render(request, "events/new.html.j2")
