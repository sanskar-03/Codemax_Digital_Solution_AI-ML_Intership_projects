from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    path("", views.subjects, name="subjects"),
    path("create/", views.create_subject, name="create_subject"),
    path("<int:subject_id>/", views.subject_detail, name="subject_detail"),
    path("<int:subject_id>/topic/create/", views.create_topic, name="create_topic"),
    path("topic/<int:topic_id>/complete/", views.complete_topic, name="complete_topic"),
]
