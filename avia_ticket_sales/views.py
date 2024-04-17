from django.shortcuts import render

# Create your views here.


def test(request):
    return render(request, 'avia_ticket_sales/aboba.html')