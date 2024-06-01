from django.db.models import OuterRef, Subquery, Sum, F
from openticket.models import Event, Order
from dataclasses import dataclass


@dataclass
class Paginator:
	page: int
	per_page: int


def get_events_index(paginator: Paginator):
	sold_total = Order.objects.filter(event=OuterRef('pk')).values('event')
	sold_total_per_event = Subquery(sold_total.annotate(sold_total=Sum('number_of_tickets')).values('sold_total'))
	offset = (paginator.page-1)*paginator.per_page
	return Event.objects.annotate(avail_total=F('number_of_tickets')-sold_total_per_event)[offset:paginator.per_page]
