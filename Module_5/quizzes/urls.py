from django.urls import path
from . import views

app_name = "quizzes"

urlpatterns = [
    path("", views.quiz_home, name="home"),
    path("topic/<int:topic_id>/", views.take_quiz, name="take"),
    path("result/<int:attempt_id>/", views.result, name="result"),
]
