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