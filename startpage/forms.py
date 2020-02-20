from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username',
                                                             'placeholder': 'Wprowadź login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'userpassword',
                                                                 'placeholder': 'Wprowadź hasło'}))


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username',
                                                             'placeholder': 'Wprowadź login'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'useremail',
                                                             'placeholder': 'Wprowadź email'}))
    email_confirm = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'conf-useremail',
                                                             'placeholder': 'Powtórz email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'userpassword',
                                                                 'placeholder': 'Wprowadź hasło'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'conf_password',
                                                                 'placeholder': 'Powtórz hasło'}))
    from_where = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'from_where',
                                                             'placeholder': 'Wpisz tutaj...'}))

    def clean(self):

        email = self.cleaned_data['email']
        email_confirm = self.cleaned_data['email_confirm']

        if email != email_confirm:
            raise forms.ValidationError("Emails must match")

        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']

        if password != password_confirm:
            raise forms.ValidationError("Passwords must match")

        return self.cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Imie'}))
    your_email = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twój email'}))
    subject = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Temat', }))
    text = forms.CharField(label='Email', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Treść wiadomości', 'rows': 4}))

