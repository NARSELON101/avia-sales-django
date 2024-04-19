from django.db.models import QuerySet
from django.shortcuts import render, redirect

from users.models import User
from kayak_ticket_parser import main as parse_tickets
# Create your views here.


def index(request):
    return render(request, 'avia_ticket_sales/layout.html')


def login_page(request):
    user = request.GET.get("username")
    password = request.GET.get("password")
    if user and password:
        return redirect('/api/docs')
    else:
        return render(request, 'avia_ticket_sales/login_page.html')


def registration_page(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email = request.GET.get("email")
    password = request.GET.get("password")
    if all([first_name, last_name, email, password]):
        print("SUCCESS")
        users_email: QuerySet = User.objects.values_list('email', flat=True)
        if email not in users_email:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            new_user.save()
        else:
            return render(request, 'avia_ticket_sales/registration.html',
                          context={"error": "Введеный Email уже занят"})
    else:
        return render(request, 'avia_ticket_sales/registration.html')


def reserve_tickets(request):
    parse_tickets()
    return render(request, 'avia_ticket_sales/cards.html')