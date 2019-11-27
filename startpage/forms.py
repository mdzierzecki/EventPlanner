from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.layout import  Submit, Fieldset, Layout, Div


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    email_confirm = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    from_where = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-user-register-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Log in',
                     Field('username', css_class="some-class"),
                     Field('email', css_class="some-class"),
                     Field('email_confirm', css_class="some-class"),
                     Field('password', css_class="some-class"),
                     Field('password_confirm', css_class="some-class")),
        )

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