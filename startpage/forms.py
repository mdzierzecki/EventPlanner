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
                                                             'placeholder': 'Skad jestes'}))

    def clean(self):
        print(self.cleaned_data)

        email = self.cleaned_data['email']
        email_confirm = self.cleaned_data['email_confirm']

        if email != email_confirm:
            raise forms.ValidationError("Emails must match")

        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']

        if password != password_confirm:
            raise forms.ValidationError("Passwords must match")

        return self.cleaned_data