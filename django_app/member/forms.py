from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        label='비밀번호',
        max_length=30,
        widget=forms.PasswordInput
    )
