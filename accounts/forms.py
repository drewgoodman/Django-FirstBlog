from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)
    email_confirm = forms.EmailField(widget=forms.EmailInput,label="Confirm Email")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email_confirm',
            'password',
            'password_confirm'
        ]

    # def clean(self, *args, **kwargs):
    #     validation goes here
    #     same as below,  but validation errors wont appear below the respective fields
    #     return super(UserRegisterForm, self).clean(*args, **kwargs)

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("This email has already been registered.")
    #     return email

    def clean_email_confirm(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email_confirm')
        email_qs = User.objects.filter(email=email)
        if email != email2:
            raise forms.ValidationError("Emails must match.")
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered.")
        return email2
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')
        if password != password2:
            raise forms.ValidationError("Passwords must match.")
        return password2