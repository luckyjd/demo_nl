from django.urls import path

from . import views

urlpatterns = [
    path("", views.lock_meeting_view, name="lock_meeting"),
]
