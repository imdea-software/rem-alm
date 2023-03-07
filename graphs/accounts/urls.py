from django.urls import path
from . import views

urlpatterns = [
    path('activate_user',views.activate_user_profile, name="activate-user"),
]