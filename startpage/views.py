from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.models import User, Group
from .models import eUser
from .forms import UserRegisterForm
from django.db import IntegrityError
from django.forms.utils import ErrorList

def startpage(request):
    return render(request, 'homepage.html')


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
            return redirect('/login')
        except IntegrityError:
            form._errors['username'] = ErrorList(['Username "{}" is already in use'.format(username)])

        return super(UserRegisterView, self).form_invalid(form)