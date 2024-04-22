from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from . token import generate_token
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail

from avia_ticket_sales import settings
from avia_ticket_sales.forms import AuthUserForm, RegisterUserForm
from kayak_ticket_parser import main as parse_tickets
# Create your views here.


def index(request):
    return render(request, 'avia_ticket_sales/layout.html')


class LoginUser(LoginView):
    form_class = AuthUserForm
    template_name = 'avia_ticket_sales/login_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


def signin(request):
    # Проверка, что пользователь зашел в акк
    print(request.user.is_authenticated)
    # TODO Сделать redirect в личный кабинет пользователя
    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["password"]
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            username = user.username
            return redirect("tickets")

        else:
            messages.error(request, "Пользователя не существует")
            return render(request, "avia_ticket_sales/login_page.html", context={"form": AuthUserForm})
    print("AAAA")
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
            print(User.objects.filter(username=username).exists())
            messages.error(request, "Username already exist! Please try some other username.")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        if User.objects.filter(email=email).exists():
            print(User.objects.filter(email=email).exists())

            messages.error(request, "Email Already Registered!!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        if len(username) > 20:
            print(len(username) > 20)
            messages.error(request, "Username must be under 20 charcters!!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        if password1 != password2:
            print(password1 == password2)
            messages.error(request, "Passwords didn't matched!!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.is_active = False
        myuser.save()
        print(myuser.pk)
        # Email Address Confirmation Email
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ FiftyBit - Django Login!!"
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
        return render(request, "avia_ticket_sales/login_page.html", context={"form": AuthUserForm})

    return render(request, 'avia_ticket_sales/registration.html', context={'form': RegisterUserForm})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(e)
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'avia_ticket_sales/registration.html'
    success_url = reverse_lazy('test')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login_page(self.request, user)
        return redirect('home')


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