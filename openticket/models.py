from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    number_of_tickets = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Order(models.Model):
    session_id = models.CharField(max_length=32)
    event = models.ForeignKey(Event, db_constraint=False, on_delete=models.DO_NOTHING)
    number_of_tickets = models.IntegerField()
    purchased_at = models.DateTimeField()
