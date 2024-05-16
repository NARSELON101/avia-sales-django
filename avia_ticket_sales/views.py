import datetime
import os

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.defaultfilters import register
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView
from kayak_ticket_parser import main as parse_tickets
from django.views.generic import ListView, CreateView

from avia_ticket_sales import settings
from avia_ticket_sales.forms import AuthUserForm, RegisterUserForm
from tickets.models import Ticket, TicketNotify
from .token import generate_token


# Create your views here.


def index(request):
    return render(request, 'avia_ticket_sales/layout.html')


def signin(request):
    # Проверка, что пользователь зашел в акк
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["password"]
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect("profile")

        else:
            messages.error(request, "Пользователя не существует")
            return render(request, "avia_ticket_sales/login_page.html", context={"form": AuthUserForm})
    return render(request, "avia_ticket_sales/login_page.html", context={"form": AuthUserForm})


class RegistrationView(CreateView):
    form_class = RegisterUserForm
    template_name = 'avia_ticket_sales/registration.html'
    success_url = reverse_lazy('login_page')

    def post(self, request, *args, **kwargs):
        # user cant register new users if he authorized
        if request.user.is_authenticated:
            messages.error(request, "Данный логин уже занят!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        my_user = form.save()
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        current_site = get_current_site(self.request)
        email_subject = "Подтверждение регистрации ADJ Sales Company"
        message2 = render_to_string('avia_ticket_sales/email_confirm.html', {
            'name': my_user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generate_token.make_token(my_user)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [my_user.email],
        )
        send_mail(email_subject, message2, from_email, to_list, fail_silently=True)
        return render(self.request, 'avia_ticket_sales/acc_activate_page.html')

    def form_invalid(self, form):
        if "username" in form.errors:
            messages.error(self.request, "Данный логин уже занят!")
            return render(self.request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})
        if "password2" in form.errors:
            messages.error(self.request, "Введенные пароли не совпадают!")
            return render(self.request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})
        # etc
        return super().form_invalid(form)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        my_user = None

    if my_user is not None and generate_token.check_token(my_user, token):
        my_user.is_active = True
        my_user.save()
        login(request, my_user)
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


def reserve_tickets(request):
    if request.user.is_authenticated:
        # parse_tickets()
        return render(request, 'avia_ticket_sales/cards.html')
    else:
        messages.error(request, 'Для доступа к бронированию авторизуйтесь на сайте')
        return redirect('signin')


class TicketsView(LoginRequiredMixin, ListView):
    model = Ticket
    paginate_by = 5
    template_name = 'avia_ticket_sales/cards.html'

    context_object_name = 'tickets'

    def handle_no_permission(self):
        messages.error(self.request, 'Для доступа к бронированию авторизуйтесь на сайте')
        return redirect('signin')

    def get_queryset(self):
        return Ticket.objects.filter(user_model__isnull=True)


def user_profile(request):
    return render(request, 'avia_ticket_sales/user_profile.html', context={"user": request.user})


def reserve_ticket(request, ticket_uid):
    ticket = Ticket.objects.get(ticket_uid=ticket_uid)

    if not eval(os.environ.get("AUTO_CONFIRM", True)):
        ticket.is_confirmed = False
        ticket.reserve_time = datetime.datetime.now()

    ticket.user_model = request.user

    ticket.save()

    return redirect('tickets')


def cancel_reserve_ticket(request, ticket_uid):
    try:
        ticket_notify = TicketNotify.objects.get(ticket_uid=ticket_uid)
        ticket_notify.delete()
    except TicketNotify.DoesNotExist:
        pass

    ticket = Ticket.objects.get(ticket_uid=ticket_uid)
    ticket.user_model = None
    ticket.reserve_time = None
    ticket.is_confirmed = True
    ticket.save()
    return redirect('user_tickets')


def add_notify(request, ticket_uid):
    ticket_obj = Ticket.objects.get(ticket_uid=ticket_uid)
    notify_obj = TicketNotify(ticket_uid=ticket_obj, user_uid=request.user,
                              notify_delay=request.POST.get("notify"))
    notify_obj.save()
    return redirect("user_tickets")


def cancel_notify(request, ticket_uid):
    try:
        ticket_notify = TicketNotify.objects.get(ticket_uid=ticket_uid)
        ticket_notify.delete()
    except TicketNotify.DoesNotExist:
        pass

    return redirect('user_tickets')


def user_tickets(request):
    return render(request, 'avia_ticket_sales/user_tickets.html', context={'ticket_notify': TicketNotify.objects})


def user_logout(request):
    logout(request)
    return redirect('signin')


@register.filter
def ticket_notifies(things, ticket):
    try:
        result = things.get(ticket_uid=ticket)
    except TicketNotify.DoesNotExist:
        result = None
    return result
