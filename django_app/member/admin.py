from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import MyUser


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'nickname')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'gender', 'nickname')}),
    )
    # 이메일을 받을 수 있게 추가
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )


admin.site.register(MyUser, MyUserAdmin)
