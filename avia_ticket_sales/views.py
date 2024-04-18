from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'avia_ticket_sales/layout.html')


def login_page(request):
    return render(request, 'avia_ticket_sales/login_page.html')
