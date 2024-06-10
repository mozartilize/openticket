from dataclasses import dataclass

from django.db.models import OuterRef, Subquery, Sum, F
from django import forms

from openticket.models import Event, Order


class EventsFilter(forms.Form):
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
            self.fields[f].widget.attrs['class'] = 'form-control'

    def full_clean(self) -> None:
        super().full_clean()
        if not self.cleaned_data['page']:
            self.cleaned_data['page'] = 1


@dataclass
class Paginator:
    page: int = 1
    per_page: int = 20


@dataclass
class EventsFilterInput(Paginator):
    name: str = ''
    start_date: str = ''
    order_by: str = ''


def get_events_index(filter: EventsFilterInput):
    sold_total = Order.objects.filter(event=OuterRef("pk")).values("event")
    sold_total_per_event = Subquery(
        sold_total.annotate(sold_total=Sum("number_of_tickets")).values("sold_total")
    )
    offset = (filter.page - 1) * filter.per_page
    base_qs = Event.objects.all()
    if filter.name:
        base_qs = base_qs.filter(name__icontains=filter.name)
    if filter.start_date:
        base_qs = base_qs.filter(start_date__gte=filter.start_date)
    if filter.order_by:
        base_qs = base_qs.order_by(filter.order_by)
    return (
        base_qs
        .annotate(avail_total=F("number_of_tickets") - sold_total_per_event)[
            offset : filter.per_page
        ]
    )
