from django.contrib import admin
from tickets.models import Ticket, TicketNotify


# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_uid"
                    , "from_country"
                    , "to_country"
                    , 'price'
                    , "fly_time"
                    , "flight_date"
                    , "back_date"
                    , "allowed"
                    , "user_model"
                    , "is_notified"
                    , "is_confirmed"
                    , "reserve_time")

    actions = ['confirm_tickets', "deny_tickets"]

    def confirm_tickets(self, request, queryset):
        for ticket in queryset:
            ticket.reserve_time = None
            ticket.is_confirmed = True
            ticket.save()

    def deny_tickets(self, request, queryset):
        for ticket in queryset:
            ticket.user_model = None
            ticket.save()

    pass


@admin.register(TicketNotify)
class TicketNotifyAdmin(admin.ModelAdmin):
    pass
