from django.conf.urls import url
from . import views

# 네임스페이스 지정
app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login_fbv, name='login'),
    url(r'^signup/$', views.signup_fbv, name='signup'),
    url(r'^logout/$', views.logout_fbv, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
]
