from django.urls import path
from . import views

app_name = "focus"

urlpatterns = [
    path("", views.start_session, name="start"),
    path("<int:session_id>/timer/", views.timer, name="timer"),
    path("<int:session_id>/complete/", views.complete_session, name="complete"),
]
