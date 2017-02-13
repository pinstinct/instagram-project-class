from django.conf.urls import url
from . import views

# 네임스페이스 지정
app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
]
