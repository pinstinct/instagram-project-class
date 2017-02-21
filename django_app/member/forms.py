from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

from .models import MyUser


class ProfileImageForm(forms.Form):
    img_profile = forms.ImageField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        label='비밀번호',
        max_length=30,
        widget=forms.PasswordInput
    )


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=40, required=False)
    gender = forms.ChoiceField(
        choices=MyUser.CHOICES_GENDER,
        widget=forms.RadioSelect()
    )
    nickname = forms.CharField(max_length=20)

    def clean_username(self):
        """
        username field 검증 로직
        """
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError('username already exists!')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        validate_password(password1)
        if password1 != password2:
            raise forms.ValidationError('password1 and password2 not equal!')
        return password2

    def create_user(self):
        username = self.cleaned_data['username']
        password2 = self.cleaned_data['password2']
        email = self.cleaned_data['email']
        gender = self.cleaned_data['gender']
        nickname = self.cleaned_data['nickname']

        user = MyUser.objects.create_user(
            username=username,
            password=password2
        )
        user.email = email
        user.gender = gender
        user.nickname = nickname
        user.save()
        return user


class SignupModelForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'gender',
            'nickname',
        )


class ChangeProfileImageModelForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = (
            'img_profile',
        )
