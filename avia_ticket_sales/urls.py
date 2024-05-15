"""
URL configuration for avia_ticket_sales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views, settings

urlpatterns = [
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    path('admin/', admin.site.urls),
    path('',  views.index, name='home'),
    path("signup/", views.RegistrationView.as_view(), name='signup'),
    path("signin/", views.signin, name='signin'),

   # path('test/', views.reserve_tickets, name='tickets'),

    path('tickets/', views.TicketsView.as_view(), name='tickets'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("profile/", views.user_profile, name='profile'),
    path("logout/", views.user_logout, name='logout'),
    path('user_tickets/', views.user_tickets, name='user_tickets'),
    path("reserve_ticket/<ticket_uid>", views.reserve_ticket, name='ticket_reserve'),
    path("cancel_reserve_ticket/<ticket_uid>", views.cancel_reserve_ticket, name='cansel_reserve_ticket'),
    path("add_notify/<ticket_uid>", views.add_notify, name='notify'),
    path("cancel_notify/<ticket_uid>", views.cancel_notify, name='cancel_notify')
]
