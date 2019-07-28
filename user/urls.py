from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Profile.as_view(), name='profile'),
    url(r'^sign-in/$', views.SignIn.as_view(), name='sign-in'),
    url(r'^sign-out/$', views.SignOut.as_view(), name='sign-in'),
    url(r'^sign-up/$', views.SignUp.as_view(), name='sign-up'),

]
