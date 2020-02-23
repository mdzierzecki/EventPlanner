from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, View
from django.contrib.auth.models import User, Group
from events.models import Event
from .models import eUser
from .forms import UserRegisterForm, UserLoginForm, ContactForm, LandingContactForm
from django.db import IntegrityError
from django.forms.utils import ErrorList
from django.contrib.auth import (authenticate,
                                 login,
                                 logout,
                                 )
from django.core.mail import send_mail


def startpage(request):
    return render(request, 'homepage.html')


def howitworks_startpage_view(request):
    return render(request, 'howitworks.html')


def faq_startpage_view(request):
    return render(request, 'faq.html')


def logout_view(request):
    logout(request)
    return redirect('/')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {

            'form': form
        })

    def post(self, request):
        fail = 'Wrong username or password'
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if len(Event.objects.filter(author=user)) <= 1:
                    return HttpResponseRedirect(reverse('event_add_view'))
                else:
                    return HttpResponseRedirect(reverse('user_events_list'))
            else:
                messages.error(request, "Niepoprawne dane logowania. Spróbuj ponownie")

        return render(request, self.template_name, {

            'form': form,
            'fail': fail
        })


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'register_account.html'

    def form_valid(self, form):
        try:

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            from_where = form.cleaned_data['from_where']
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            iUser = eUser(user=user, from_where=from_where)
            iUser.save()
            user.save()
            messages.add_message(self.request, messages.SUCCESS, 'Dziękujemy za rejestrację. Poniżej możesz zalogować się podanymi danymi')
            return redirect('/login')
        except IntegrityError:
            form._errors['username'] = ErrorList(['Użytkownik "{}" już istnieje'.format(username)])

        return super(UserRegisterView, self).form_invalid(form)


def user_help_view(request):
    return render(request, 'help.html')


def contact_success_view(request):
    return render(request, 'contact/contact_success.html')


def contact_error_view(request):
    return render(request, 'contact/contact_error.html')


def contact_view(request):

    form = ContactForm(request.POST)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = ContactForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            try:
                email = send_mail(
                    'ZipEvent Kontakt: {}'.format(form.cleaned_data['subject']),
                    'Name: {}, From email: {} , Message: {} '.format(form.cleaned_data['name'], form.cleaned_data['your_email'], form.cleaned_data['text']),
                    'ZipEvent Team <no-reply@slickcode.pl>',
                    ['kontakt@slickcode.pl'],
                    fail_silently=False,
                )
                if email == 1:
                    return HttpResponseRedirect(reverse('contact_success_view'))
                else:
                    return HttpResponseRedirect(reverse('contact_error_view'))
            except:
                return HttpResponseRedirect(reverse('contact_error_view'))
    context = {
        'form': form,
    }

    return render(request, 'contact/contact.html', context)


def contact_startpage_view(request):

    form = LandingContactForm(request.POST)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = LandingContactForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            try:
                email = send_mail(
                    'ZipEvent Kontakt',
                    'Name: {}, From email: {} , Message: {} '.format(form.cleaned_data['name'], form.cleaned_data['your_email'], form.cleaned_data['text']),
                    'ZipEvent Team <no-reply@slickcode.pl>',
                    ['kontakt@slickcode.pl'],
                    fail_silently=False,
                )
                if email == 1:
                    return HttpResponseRedirect(reverse('contact_startpage_success_view'))
                else:
                    return HttpResponseRedirect(reverse('contact_startpage_error_view'))
            except:
                return HttpResponseRedirect(reverse('contact_startpage_error_view'))
    context = {
        'form': form,
    }

    return render(request, 'contact/contact_startpage.html', context)


def contact_startpage_success_view(request):
    return render(request, 'contact/contact_startpage_success.html')


def contact_startpage_error_view(request):
    return render(request, 'contact/contact_startpage_error.html')