from django.conf.urls import url

from . import views

# 네임스페이스 지정
app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login_fbv, name='login'),
    url(r'^signup/$', views.signup_fbv, name='signup'),
    url(r'^signup-modelform/$', views.signup_model_form_fbv, name='signup_modelform'),
    url(r'^logout/$', views.logout_fbv, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/image/$', views.change_profile_image, name='profile_image')
]
