from django.conf.urls import url
from . import views

# 네임스페이스 지정
app_name = 'post'
urlpatterns = [
    url(r'^$', views.post_list, name='list'),
]
