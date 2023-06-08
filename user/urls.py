from django.urls import path

from .views import *

urlpatterns = [
    path('singin/',signin, name='signin'),
    path('signup/',signup, name='signup'),
    path('signout/',signout, name='signout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
