
from django.conf.urls import url
from user import views
urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^emails/verification/$', views.EmailActiveView.as_view(), name='verification')
]
