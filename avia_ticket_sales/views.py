from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView

from avia_ticket_sales import settings
from avia_ticket_sales.forms import AuthUserForm, RegisterUserForm
from tickets.models import Ticket
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


def signup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if User.objects.filter(username=username):
            messages.error(request, "Данный логин уже занят!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email уже зарегистрирован!!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        if len(username) > 20:
            messages.error(request, "Логин пользователя должен содержать меньше 20 символов!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        if password1 != password2:
            messages.error(request, "Введенные пароли не совпадают!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        if not username.isalnum():
            messages.error(request, "Имя пользователя должно содержать только буквы и цифры!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.is_active = False
        myuser.save()
        # Email Address Confirmation Email
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        current_site = get_current_site(request)
        email_subject = "Подтверждение регистрации ADJ Sales Company"
        message2 = render_to_string('avia_ticket_sales/email_confirm.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        send_mail(email_subject, message2, from_email, to_list, fail_silently=True)
        return render(request, 'avia_ticket_sales/acc_activate_page.html')

    return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
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


def user_profile(request):
    return render(request, 'avia_ticket_sales/user_profile.html', context={"user": request.user})


def reserve_ticket(request, ticket_uid):
    ticket = Ticket.objects.get(ticket_uid=ticket_uid)
    ticket.user_model = request.user
    ticket.save()
    return redirect('home')


def user_tickets(request):
    return render(request, 'avia_ticket_sales/user_tickets.html')


def user_logout(request):
    logout(request)
    return redirect('signin')
