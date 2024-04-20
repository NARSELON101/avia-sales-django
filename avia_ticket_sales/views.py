from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from avia_ticket_sales.forms import AuthUserForm, RegisterUserForm
from avia_ticket_sales.token import account_activation_token
from users.models import User
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


def signup(request):
    if request.method == 'POST':
        template = LoginUser()
        form = template.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('avia_ticket_sales/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        template = RegisterUser
        form = RegisterUserForm()
    return render(request, 'avia_ticket_sales/registration.html')


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