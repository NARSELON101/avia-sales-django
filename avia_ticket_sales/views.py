from django.shortcuts import render, redirect

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
        return render(request, 'avia_ticket_sales/registration.html')
    else:
        return render(request, 'avia_ticket_sales/registration.html')


def reserve_tickets(request):
    return render(request, 'avia_ticket_sales/cards.html')