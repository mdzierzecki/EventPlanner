from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, View
from django.contrib.auth.models import User, Group
from .models import eUser
from .forms import UserRegisterForm, UserLoginForm
from django.db import IntegrityError
from django.forms.utils import ErrorList
from django.contrib.auth import (authenticate,
                                 login,
                                 logout,
                                 )


def startpage(request):
    return render(request, 'homepage.html')


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
            form._errors['username'] = ErrorList(['Username "{}" is already in use'.format(username)])

        return super(UserRegisterView, self).form_invalid(form)