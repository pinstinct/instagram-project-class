from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username
        )
        user.set_password(password)
        # admin 페이지에 접속할 수 있는 권한에 대한 관리
        user.is_staff = True
        # admin 페이지를 사용할 수 있는 모든 권한 부여
        user.is_superuser = True
        user.save()
        return user


# 다중상속을 받음
class MyUser(PermissionsMixin, AbstractBaseUser):
    CHOICES_GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    # 기본 값 (3개)
    # password / last_login / is_active
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    nickname = models.CharField(max_length=20)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    object = MyUserManager()

    def get_full_name(self):
        return '{} ({})'.format(
            self.nickname,
            self.username,
        )

    def get_short_name(self):
        return self.nickname
