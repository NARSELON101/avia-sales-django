from django.contrib import admin

from tickets.models import Ticket


# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass
