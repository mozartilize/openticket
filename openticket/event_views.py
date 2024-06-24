from typing import Any

from django.http import HttpRequest, Http404
from django.http.response import HttpResponse
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.views import View

from openticket.models import Event
from openticket.lib.events_service import (
    NewEventForm,
    get_events_index,
    EventsFilter,
    EventsFilterInput,
)
from openticket.lib.view_shortcuts import redirect_to


def index(request: HttpRequest):
    return render(request, "index.html.j2")


class EventBaseView(View):
    events_filter: EventsFilter
    events_filter_input: EventsFilterInput

    def get_handler(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        self.events_filter = EventsFilter(data=request.GET, initial=request.GET)

        if not self.events_filter.is_valid():
            raise BadRequest("Invalid params")

        self.events_filter_input = EventsFilterInput(**self.events_filter.cleaned_data)

        return handler

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = self.get_handler(request, *args, **kwargs)
        return handler(request, *args, **kwargs)


class EventView(EventBaseView):
    def get_handler(self, request: HttpRequest, *args: Any, **kwargs: Any):
        handler = super().get_handler(request, *args, **kwargs)

        if request.method.lower() == "post" and self.events_filter_input.id:
            handler = self.update
        elif request.method.lower() == "get" and self.events_filter_input.id:
            handler = self.detail
        return handler

    def get(self, request: HttpRequest):
        events = get_events_index(self.events_filter_input)
        return render(
            request,
            "events/index.html.j2",
            context={"events": events, "events_filter": self.events_filter},
        )

    def detail(self, request: HttpRequest):
        event = get_events_index(self.events_filter_input).first()
        if not event:
            raise Http404("Event not found")
        return render(
            request,
            "events/detail.html.j2",
            context={"event": event},
        )

    def post(self, request: HttpRequest):
        event_form = NewEventForm(data=request.POST)
        event_form.is_valid()
        event = Event(**event_form.cleaned_data)
        event.save()
        return redirect_to("events", query_params=dict(id=event.pk))

    def update(self, request: HttpRequest):
        event = get_events_index(self.events_filter_input).first()
        if not event:
            raise Http404("Event not found")
        event_form = NewEventForm(
            initial={
                "name": event.name,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "number_of_tickets": event.number_of_tickets,
            },
            data=request.POST,
        )
        event_form.is_valid()
        for k, v in event_form.cleaned_data.items():
            setattr(event, k, v)
        event.save()
        return redirect_to("events", query_params=dict(id=event.pk))


class EventHtmxView(EventBaseView):
    def get(self, request: HttpRequest):
        event = get_events_index(self.events_filter_input).first()
        if not event:
            raise Http404("Event not found")
        event_form = NewEventForm(
            initial={
                "name": event.name,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "number_of_tickets": event.number_of_tickets,
            }
        )
        return render(
            request,
            "events/htmx/_edit.html.j2",
            context={"event_form": event_form, "event": event},
        )


def event_form(request: HttpRequest):
    new_event_form = NewEventForm()
    return render(
        request, "events/new.html.j2", context={"new_event_form": new_event_form}
    )
