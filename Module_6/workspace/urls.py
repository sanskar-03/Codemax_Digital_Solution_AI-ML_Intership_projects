from django.urls import path
from . import views
urlpatterns=[
    path("",views.landing,name="landing"),
    path("dashboard/",views.home,name="home"),
    path("workspace/",views.workspace,name="workspace"),
    path("assessments/",views.assessment_history,name="assessment_history"),
    path("assessment/<int:pk>/",views.assessment_detail,name="assessment_detail"),
    path("assessment/<int:pk>/report/",views.assessment_pdf,name="assessment_pdf"),
]
