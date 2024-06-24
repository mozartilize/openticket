from dataclasses import dataclass

from django.db.models import OuterRef, Subquery, Sum, F
from django.db.models.functions import Coalesce
from django import forms

from openticket.models import Event, Order
from openticket.lib import Paginator


class NewEventForm(forms.Form):
    name = forms.CharField()
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    number_of_tickets = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs["class"] = "form-control"


class EventsFilter(forms.Form):
    id = forms.IntegerField(required=False, min_value=1)
    name = forms.CharField(required=False)
    start_date = forms.DateField(required=False)
    page = forms.IntegerField(min_value=1, required=False, initial=1)
    order_by = forms.ChoiceField(
        choices=[
            ("", "----"),
            ("name", "Name"),
            ("-name", "Name (Desc)"),
            ("start_date", "Start"),
            ("-start_date", "Start (Desc)"),
        ],
        required=False,
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs["class"] = "form-control"

    def full_clean(self) -> None:
        super().full_clean()
        if not self.cleaned_data["page"]:
            self.cleaned_data["page"] = 1


@dataclass
class EventsFilterInput(Paginator):
    id: int = 0
    name: str = ""
    start_date: str = ""
    order_by: str = ""
    edit: bool = False


def get_events_index(filter: EventsFilterInput):
    sold_total = Order.objects.filter(event=OuterRef("pk")).values("event")
    sold_total_per_event = Subquery(
        sold_total.annotate(sold_total=Sum("number_of_tickets")).values("sold_total")
    )
    offset = (filter.page - 1) * filter.per_page
    base_qs = Event.objects.annotate(
        avail_total=F("number_of_tickets") - Coalesce(sold_total_per_event, 0)
    )
    if filter.id:
        return base_qs.filter(id=filter.id)
    if filter.name:
        base_qs = base_qs.filter(name__icontains=filter.name)
    if filter.start_date:
        base_qs = base_qs.filter(start_date__gte=filter.start_date)
    if filter.order_by:
        base_qs = base_qs.order_by(filter.order_by)
    return base_qs[offset : filter.per_page]
