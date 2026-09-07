from django.contrib import admin
from django.urls import include, path
from dashboard.views import landing

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", landing, name="home"),

    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("learning/", include("learning.urls")),
    path("ai/", include("ai_engine.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("focus/", include("focus.urls")),
    path("recommendations/", include("recommendations.urls")),
    path("reports/", include("reports.urls")),
]
