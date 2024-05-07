from django.contrib import admin

from tickets.models import Ticket, TicketNotify


# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(TicketNotify)
class TicketNotifyAdmin(admin.ModelAdmin):
    pass
