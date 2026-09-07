#!/usr/bin/env python
"""
TRAVELSHIELD COMPLETE AUTOMATED FIX
Fixes:
- Broken/raw Django CSS
- Landing page
- Sign up
- Sign in
- Sign out
- Dashboard
- Assessment form
- Assessment history
- Assessment result page
- Responsive mobile navigation
- Better human-made professional UI
- Optional Celery import so Django can run without Celery installed

SAVE AS:

fix_travelshield_everything.py

RUN:

cd C:\AI_PROJECTS\FINAL_PROJECTS\travelshield

.venv\Scripts\python.exe fix_travelshield_everything.py

THEN:

.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
"""

from pathlib import Path
from datetime import datetime
import shutil
import textwrap

ROOT = Path(__file__).resolve().parent
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / f"backup_before_complete_fix_{STAMP}"


def backup_and_write(relative_path, content):
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        backup_path = BACKUP / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)

    path.write_text(
        textwrap.dedent(content).lstrip(),
        encoding="utf-8"
    )


# ============================================================
# 1. WORKSPACE FORMS
# ============================================================

backup_and_write(
    "workspace/forms.py",
    """
    from django import forms
    from .models import TravelAssessment


    class AssessmentForm(forms.ModelForm):

        class Meta:
            model = TravelAssessment

            fields = [
                "origin",
                "destination",
                "duration_days",
                "budget",
                "weather_risk",
                "crowd_level",
                "transport_reliability",
                "season",
            ]

            widgets = {

                "origin": forms.TextInput(
                    attrs={
                        "placeholder": "Delhi",
                    }
                ),

                "destination": forms.TextInput(
                    attrs={
                        "placeholder": "Manali",
                    }
                ),

                "duration_days": forms.NumberInput(
                    attrs={
                        "min": 1,
                        "max": 90,
                        "placeholder": "5",
                    }
                ),

                "budget": forms.NumberInput(
                    attrs={
                        "min": 1000,
                        "step": 500,
                        "placeholder": "40000",
                    }
                ),

                "weather_risk": forms.NumberInput(
                    attrs={
                        "min": 1,
                        "max": 10,
                        "placeholder": "1 to 10",
                    }
                ),

                "crowd_level": forms.NumberInput(
                    attrs={
                        "min": 1,
                        "max": 10,
                        "placeholder": "1 to 10",
                    }
                ),

                "transport_reliability": forms.NumberInput(
                    attrs={
                        "min": 1,
                        "max": 10,
                        "placeholder": "1 to 10",
                    }
                ),

                "season": forms.Select(
                    choices=[
                        ("winter", "Winter"),
                        ("spring", "Spring"),
                        ("summer", "Summer"),
                        ("monsoon", "Monsoon"),
                    ]
                ),
            }

            labels = {
                "origin": "Starting city",
                "destination": "Destination",
                "duration_days": "Trip duration (days)",
                "budget": "Trip budget (₹)",
                "weather_risk": "Weather exposure",
                "crowd_level": "Expected crowding",
                "transport_reliability": "Transport reliability",
                "season": "Travel season",
            }

            help_texts = {
                "weather_risk":
                    "1 = very low weather exposure · 10 = severe weather exposure",

                "crowd_level":
                    "1 = quiet · 10 = extremely crowded",

                "transport_reliability":
                    "1 = unreliable · 10 = highly reliable",
            }

        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)

            for field in self.fields.values():
                field.widget.attrs["class"] = "field-control"
    """
)


# ============================================================
# 2. AUTHENTICATION
# ============================================================

backup_and_write(
    "accounts/views.py",
    """
    from urllib.parse import urlparse

    from django.contrib import messages
    from django.contrib.auth import authenticate, login, logout
    from django.contrib.auth.forms import UserCreationForm
    from django.shortcuts import redirect, render


    def safe_next_url(request, default="home"):

        next_url = (
            request.POST.get("next")
            or request.GET.get("next")
        )

        if next_url:

            parsed = urlparse(next_url)

            if not parsed.netloc and next_url.startswith("/"):
                return next_url

        return default


    def login_view(request):

        if request.user.is_authenticated:
            return redirect("home")

        if request.method == "POST":

            username = request.POST.get(
                "username",
                ""
            ).strip()

            password = request.POST.get(
                "password",
                ""
            )

            if not username or not password:

                messages.error(
                    request,
                    "Please enter both username and password."
                )

            else:

                user = authenticate(
                    request,
                    username=username,
                    password=password
                )

                if user is not None:

                    login(request, user)

                    messages.success(
                        request,
                        f"Welcome back, {user.username}."
                    )

                    return redirect(
                        safe_next_url(request)
                    )

                messages.error(
                    request,
                    "The username or password is incorrect."
                )

        return render(
            request,
            "accounts/login.html",
            {
                "next": request.GET.get("next", "")
            }
        )


    def register_view(request):

        if request.user.is_authenticated:
            return redirect("home")

        form = UserCreationForm(
            request.POST or None
        )

        if request.method == "POST":

            if form.is_valid():

                user = form.save()

                login(request, user)

                messages.success(
                    request,
                    "Your account has been created successfully."
                )

                return redirect("home")

            messages.error(
                request,
                "Please correct the highlighted information."
            )

        for field in form.fields.values():

            field.widget.attrs["class"] = "field-control"

        return render(
            request,
            "accounts/register.html",
            {
                "form": form
            }
        )


    def logout_view(request):

        if request.method == "POST":

            logout(request)

            messages.success(
                request,
                "You have been signed out successfully."
            )

        return redirect("landing")
    """
)


# ============================================================
# 3. BASE TEMPLATE
# ============================================================

backup_and_write(
    "templates/base.html",
    """
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            {% block title %}TravelShield{% endblock %}
        </title>

        <link
            rel="stylesheet"
            href="{% static 'app.css' %}"
        >

    </head>


    <body>

        <header class="topbar">

            <div class="shell nav-shell">

                <a
                    class="brand"
                    href="{% if user.is_authenticated %}{% url 'home' %}{% else %}{% url 'landing' %}{% endif %}"
                >

                    <span class="brand-badge">
                        TS
                    </span>

                    <span>
                        TravelShield
                    </span>

                </a>


                <button
                    class="menu-toggle"
                    type="button"
                    aria-label="Open navigation"
                >
                    Menu
                </button>


                <nav class="nav-links">

                    {% if user.is_authenticated %}

                        <a href="{% url 'home' %}">
                            Dashboard
                        </a>

                        <a href="{% url 'workspace' %}">
                            New assessment
                        </a>

                        <a href="{% url 'assessment_history' %}">
                            My trips
                        </a>


                        {% if user.is_staff %}

                            <a href="/admin/">
                                Administration
                            </a>

                        {% endif %}


                        <form
                            method="post"
                            action="{% url 'logout' %}"
                            class="logout-form"
                        >

                            {% csrf_token %}

                            <button
                                type="submit"
                                class="nav-signout"
                            >
                                Sign out
                            </button>

                        </form>


                    {% else %}

                        <a href="{% url 'login' %}">
                            Sign in
                        </a>

                        <a
                            href="{% url 'register' %}"
                            class="nav-cta"
                        >
                            Create account
                        </a>

                    {% endif %}

                </nav>

            </div>

        </header>


        {% if messages %}

            <div class="shell flash-wrap">

                {% for message in messages %}

                    <div class="flash {{ message.tags }}">

                        {{ message }}

                    </div>

                {% endfor %}

            </div>

        {% endif %}


        <main>

            {% block content %}
            {% endblock %}

        </main>


        <footer class="footer">

            <div class="shell footer-inner">

                <div>

                    <strong>
                        TravelShield
                    </strong>

                    <span>
                        Travel risk, safety and disruption planning.
                    </span>

                </div>

                <span>
                    © {% now "Y" %} TravelShield
                </span>

            </div>

        </footer>


        <script>

            const menuButton =
                document.querySelector(".menu-toggle");

            const navigation =
                document.querySelector(".nav-links");

            if (menuButton && navigation) {

                menuButton.addEventListener(
                    "click",
                    function () {

                        navigation.classList.toggle("open");

                    }
                );

            }

        </script>


        {% block scripts %}
        {% endblock %}

    </body>

    </html>
    """
)


# ============================================================
# 4. LANDING PAGE
# ============================================================

backup_and_write(
    "templates/public/landing.html",
    """
    {% extends "base.html" %}

    {% block title %}
    TravelShield · Travel smarter
    {% endblock %}


    {% block content %}

    <section class="hero">

        <div class="shell hero-grid">

            <div>

                <p class="kicker">
                    TRAVEL RISK INTELLIGENCE
                </p>

                <h1>
                    Know the trip before you take it.
                </h1>

                <p class="lead">

                    TravelShield helps you understand
                    weather exposure, crowd pressure,
                    transport reliability and other
                    travel risks before your journey.

                </p>


                <div class="hero-actions">

                    <a
                        href="{% url 'register' %}"
                        class="button primary"
                    >
                        Assess a trip
                    </a>

                    <a
                        href="#how-it-works"
                        class="button secondary"
                    >
                        See how it works
                    </a>

                </div>


                <div class="trust-row">

                    <span>
                        Clear scores
                    </span>

                    <span>
                        Simple guidance
                    </span>

                    <span>
                        Saved trip history
                    </span>

                </div>

            </div>


            <div class="sample-card">

                <div class="sample-top">

                    <span>
                        EXAMPLE TRIP
                    </span>

                    <b>
                        Delhi → Manali
                    </b>

                </div>


                <div class="sample-score">

                    <strong>
                        82
                    </strong>

                    <span>
                        /100
                        <br>
                        trip confidence
                    </span>

                </div>


                <div class="signal">

                    <span>
                        Weather
                    </span>

                    <div>
                        <i style="width:25%"></i>
                    </div>

                    <b>
                        Low
                    </b>

                </div>


                <div class="signal">

                    <span>
                        Crowds
                    </span>

                    <div>
                        <i style="width:52%"></i>
                    </div>

                    <b>
                        Medium
                    </b>

                </div>


                <div class="signal">

                    <span>
                        Route
                    </span>

                    <div>
                        <i style="width:75%"></i>
                    </div>

                    <b>
                        High
                    </b>

                </div>


                <p class="sample-note">

                    Your trip looks possible.
                    Leaving earlier may reduce
                    congestion and travel pressure.

                </p>

            </div>

        </div>

    </section>


    <section
        id="how-it-works"
        class="section shell"
    >

        <div class="section-heading">

            <p class="kicker">
                HOW IT WORKS
            </p>

            <h2>
                Three simple steps.
            </h2>

            <p>
                You do not need to understand
                machine learning. Just describe
                your trip.
            </p>

        </div>


        <div class="feature-grid">

            <article class="feature-card">

                <span>01</span>

                <h3>
                    Tell us about your trip
                </h3>

                <p>
                    Add your route, duration,
                    budget and expected conditions.
                </p>

            </article>


            <article class="feature-card">

                <span>02</span>

                <h3>
                    Get your risk picture
                </h3>

                <p>
                    TravelShield evaluates
                    the important conditions
                    around your journey.
                </p>

            </article>


            <article class="feature-card">

                <span>03</span>

                <h3>
                    Plan with clarity
                </h3>

                <p>
                    Understand what influenced
                    your result and review
                    your trip later.
                </p>

            </article>

        </div>

    </section>


    <section class="section muted">

        <div class="shell">

            <div class="section-heading">

                <p class="kicker">
                    WHAT IS CHECKED
                </p>

                <h2>
                    One trip. A clearer picture.
                </h2>

            </div>


            <div class="risk-grid">

                <div>Weather exposure</div>

                <div>Transport disruption</div>

                <div>Destination crowding</div>

                <div>Trip duration</div>

                <div>Seasonal conditions</div>

                <div>Overall trip risk</div>

            </div>

        </div>

    </section>


    <section class="cta-section">

        <div class="shell cta-box">

            <div>

                <p class="kicker">
                    READY TO PLAN?
                </p>

                <h2>
                    Make your next travel decision
                    with more context.
                </h2>

            </div>


            <a
                href="{% url 'register' %}"
                class="button light"
            >
                Create account
            </a>

        </div>

    </section>

    {% endblock %}
    """
)


# ============================================================
# 5. LOGIN
# ============================================================

backup_and_write(
    "templates/accounts/login.html",
    """
    {% extends "base.html" %}

    {% block title %}
    Sign in · TravelShield
    {% endblock %}


    {% block content %}

    <section class="auth-page">

        <div class="auth-card">

            <p class="kicker">
                WELCOME BACK
            </p>

            <h1>
                Sign in to your trips.
            </h1>

            <p class="muted-text">
                Access your travel assessments
                and continue planning.
            </p>


            <form
                method="post"
                class="auth-form"
            >

                {% csrf_token %}

                <input
                    type="hidden"
                    name="next"
                    value="{{ next }}"
                >


                <label>

                    Username

                    <input
                        class="field-control"
                        type="text"
                        name="username"
                        required
                        autofocus
                        autocomplete="username"
                    >

                </label>


                <label>

                    Password

                    <input
                        class="field-control"
                        type="password"
                        name="password"
                        required
                        autocomplete="current-password"
                    >

                </label>


                <button
                    type="submit"
                    class="button primary full"
                >
                    Sign in
                </button>

            </form>


            <p class="auth-switch">

                New to TravelShield?

                <a href="{% url 'register' %}">
                    Create an account
                </a>

            </p>

        </div>

    </section>

    {% endblock %}
    """
)


# ============================================================
# 6. REGISTER
# ============================================================

backup_and_write(
    "templates/accounts/register.html",
    """
    {% extends "base.html" %}

    {% block title %}
    Create account · TravelShield
    {% endblock %}


    {% block content %}

    <section class="auth-page">

        <div class="auth-card">

            <p class="kicker">
                GET STARTED
            </p>

            <h1>
                Create your account.
            </h1>

            <p class="muted-text">

                Save assessments and review
                your travel decisions anytime.

            </p>


            <form
                method="post"
                class="auth-form"
                novalidate
            >

                {% csrf_token %}


                {% for field in form %}

                    <label>

                        {{ field.label }}

                        {{ field }}

                        {% if field.help_text %}

                            <small>
                                {{ field.help_text }}
                            </small>

                        {% endif %}


                        {% for error in field.errors %}

                            <span class="field-error">
                                {{ error }}
                            </span>

                        {% endfor %}

                    </label>

                {% endfor %}


                <button
                    type="submit"
                    class="button primary full"
                >
                    Create account
                </button>

            </form>


            <p class="auth-switch">

                Already have an account?

                <a href="{% url 'login' %}">
                    Sign in
                </a>

            </p>

        </div>

    </section>

    {% endblock %}
    """
)


# ============================================================
# 7. DASHBOARD
# ============================================================

backup_and_write(
    "templates/workspace/home.html",
    """
    {% extends "base.html" %}

    {% block title %}
    Dashboard · TravelShield
    {% endblock %}


    {% block content %}

    <section class="page-hero">

        <div class="shell hero-row">

            <div>

                <p class="kicker">
                    TRAVEL DASHBOARD
                </p>

                <h1>
                    Plan with confidence.
                </h1>

                <p>

                    Assess upcoming journeys,
                    understand important risk signals
                    and keep every travel decision
                    in one place.

                </p>

            </div>


            <a
                href="{% url 'workspace' %}"
                class="button primary"
            >
                + New trip assessment
            </a>

        </div>

    </section>


    <section class="shell page-section">


        <div class="stats-grid">

            <div class="stat-card">

                <span>
                    ASSESSMENTS
                </span>

                <strong>
                    {{ total }}
                </strong>

                <small>
                    Trips evaluated
                </small>

            </div>


            <div class="stat-card">

                <span>
                    HIGH-RISK TRIPS
                </span>

                <strong>
                    {{ high }}
                </strong>

                <small>
                    Need closer attention
                </small>

            </div>


            <div class="stat-card">

                <span>
                    ACTIVE MODEL
                </span>

                <strong>

                    {% if active_model %}

                        {{ active_model.version }}

                    {% else %}

                        —

                    {% endif %}

                </strong>

                <small>
                    Current prediction version
                </small>

            </div>

        </div>


        <div class="section-line">

            <div>

                <p class="kicker">
                    RECENT ACTIVITY
                </p>

                <h2>
                    Your latest assessments
                </h2>

            </div>


            <a href="{% url 'assessment_history' %}">
                View all trips →
            </a>

        </div>


        {% if recent %}

            <div class="trip-list">

                {% for item in recent %}

                    <a
                        class="trip-row"
                        href="{% url 'assessment_detail' item.id %}"
                    >

                        <div>

                            <strong>

                                {{ item.origin }}
                                →
                                {{ item.destination }}

                            </strong>

                            <small>

                                {{ item.duration_days }} days
                                ·
                                {{ item.created_at|date:"d M Y" }}

                            </small>

                        </div>


                        <div class="trip-meta">

                            <span
                                class="risk {{ item.risk_level|lower }}"
                            >
                                {{ item.risk_level }}
                            </span>

                            <b>
                                {{ item.risk_score|floatformat:0 }}/100
                            </b>

                        </div>

                    </a>

                {% endfor %}

            </div>


        {% else %}

            <div class="empty-state">

                <div class="empty-icon">
                    ✦
                </div>

                <h3>
                    No trip assessments yet
                </h3>

                <p>

                    Start with your destination.
                    TravelShield will turn your
                    trip details into a clear risk picture.

                </p>

                <a
                    href="{% url 'workspace' %}"
                    class="button primary"
                >
                    Assess my first trip
                </a>

            </div>

        {% endif %}

    </section>

    {% endblock %}
    """
)


# ============================================================
# 8. ASSESSMENT FORM
# ============================================================

backup_and_write(
    "templates/workspace/form.html",
    """
    {% extends "base.html" %}

    {% block title %}
    New assessment · TravelShield
    {% endblock %}


    {% block content %}

    <section class="shell page-section assessment-page">

        <div class="assessment-intro">

            <div>

                <p class="kicker">
                    NEW TRIP
                </p>

                <h1>
                    Check your travel plan.
                </h1>

                <p>

                    Fill in your trip details.
                    For the travel condition scores,
                    use 1 for the lowest level
                    and 10 for the highest level.

                </p>

            </div>


            <div class="progress-chip">

                <b>
                    Trip check
                </b>

                <span>
                    Complete the form
                </span>

            </div>

        </div>


        <form
            method="post"
            class="assessment-card"
        >

            {% csrf_token %}


            <div class="form-section">

                <div class="section-number">
                    01
                </div>


                <div class="form-heading">

                    <h2>
                        Route & trip
                    </h2>

                    <p>
                        Where are you going and
                        what does your trip look like?
                    </p>

                </div>


                <div class="field-grid">

                    <label>

                        {{ form.origin.label }}

                        {{ form.origin }}

                        {% for error in form.origin.errors %}

                            <span class="field-error">
                                {{ error }}
                            </span>

                        {% endfor %}

                    </label>


                    <label>

                        {{ form.destination.label }}

                        {{ form.destination }}

                        {% for error in form.destination.errors %}

                            <span class="field-error">
                                {{ error }}
                            </span>

                        {% endfor %}

                    </label>


                    <label>

                        {{ form.duration_days.label }}

                        {{ form.duration_days }}

                    </label>


                    <label>

                        {{ form.budget.label }}

                        {{ form.budget }}

                    </label>

                </div>

            </div>


            <div class="form-section">

                <div class="section-number">
                    02
                </div>


                <div class="form-heading">

                    <h2>
                        Travel conditions
                    </h2>

                    <p>
                        Give your best estimate.
                        These answers help explain
                        your final risk result.
                    </p>

                </div>


                <div class="field-grid">

                    <label>

                        {{ form.weather_risk.label }}

                        {{ form.weather_risk }}

                        <small>
                            {{ form.weather_risk.help_text }}
                        </small>

                    </label>


                    <label>

                        {{ form.crowd_level.label }}

                        {{ form.crowd_level }}

                        <small>
                            {{ form.crowd_level.help_text }}
                        </small>

                    </label>


                    <label>

                        {{ form.transport_reliability.label }}

                        {{ form.transport_reliability }}

                        <small>
                            {{ form.transport_reliability.help_text }}
                        </small>

                    </label>


                    <label>

                        {{ form.season.label }}

                        {{ form.season }}

                    </label>

                </div>

            </div>


            <div class="form-actions">

                <div>

                    <b>
                        Ready for your result?
                    </b>

                    <span>

                        Your assessment will be saved
                        in your trip history.

                    </span>

                </div>


                <button
                    type="submit"
                    class="button primary"
                >
                    Check trip risk →
                </button>

            </div>

        </form>

    </section>

    {% endblock %}
    """
)


# ============================================================
# 9. HISTORY
# ============================================================

backup_and_write(
    "templates/workspace/history.html",
    """
    {% extends "base.html" %}

    {% block title %}
    My trips · TravelShield
    {% endblock %}


    {% block content %}

    <section class="shell page-section">

        <div class="section-line">

            <div>

                <p class="kicker">
                    ASSESSMENT HISTORY
                </p>

                <h1>
                    Every trip, one clear record.
                </h1>

                <p>
                    Review previous travel risk decisions
                    and reopen any assessment.
                </p>

            </div>


            <a
                href="{% url 'workspace' %}"
                class="button primary"
            >
                + New assessment
            </a>

        </div>


        {% if assessments %}

            <div class="history-table">

                <div class="table-head">

                    <span>ROUTE</span>
                    <span>RISK</span>
                    <span>CONFIDENCE</span>
                    <span>MODEL</span>
                    <span></span>

                </div>


                {% for a in assessments %}

                    <a
                        class="table-row"
                        href="{% url 'assessment_detail' a.pk %}"
                    >

                        <div>

                            <strong>

                                {{ a.origin }}
                                →
                                {{ a.destination }}

                            </strong>

                            <small>

                                {{ a.duration_days }} days
                                ·
                                {{ a.created_at|date:"d M Y, H:i" }}

                            </small>

                        </div>


                        <div>

                            <span
                                class="risk {{ a.risk_level|lower }}"
                            >
                                {{ a.risk_level }}
                            </span>

                        </div>


                        <div>
                            {{ a.confidence|floatformat:1 }}%
                        </div>


                        <div>

                            {% if a.model_version %}

                                {{ a.model_version.version }}

                            {% else %}

                                —

                            {% endif %}

                        </div>


                        <div>
                            Open →
                        </div>

                    </a>

                {% endfor %}

            </div>


        {% else %}

            <div class="empty-state">

                <div class="empty-icon">
                    ✦
                </div>

                <h3>
                    Your trip history is empty
                </h3>

                <p>

                    Completed assessments will appear here
                    with their risk result and model version.

                </p>

                <a
                    href="{% url 'workspace' %}"
                    class="button primary"
                >
                    Create first assessment
                </a>

            </div>

        {% endif %}

    </section>

    {% endblock %}
    """
)


# ============================================================
# 10. RESULT PAGE
# ============================================================

backup_and_write(
    "templates/workspace/detail.html",
    """
    {% extends "base.html" %}

    {% block title %}
    Trip result · TravelShield
    {% endblock %}


    {% block content %}

    <section class="shell page-section result-page">


        <div class="result-header">

            <div>

                <a
                    class="back-link"
                    href="{% url 'assessment_history' %}"
                >
                    ← Back to my trips
                </a>


                <p class="kicker">
                    TRIP ASSESSMENT
                </p>


                <h1>

                    {{ assessment.origin }}
                    →
                    {{ assessment.destination }}

                </h1>


                <p>

                    {{ assessment.duration_days }} days
                    ·
                    ₹{{ assessment.budget }}
                    ·
                    {{ assessment.season|title }}

                </p>

            </div>


            <div class="result-actions">

                <a
                    href="{% url 'assessment_pdf' assessment.id %}"
                    class="button secondary"
                >
                    Download report
                </a>


                <a
                    href="{% url 'workspace' %}"
                    class="button primary"
                >
                    New assessment
                </a>

            </div>

        </div>


        <div class="result-grid">


            <article class="score-card">

                <small>
                    OVERALL TRIP RISK
                </small>


                <strong>

                    {{ assessment.risk_score|floatformat:0 }}

                    <span>
                        /100
                    </span>

                </strong>


                <span
                    class="risk {{ assessment.risk_level|lower }}"
                >

                    {{ assessment.risk_level }}
                    RISK

                </span>


                <p>

                    Model confidence:
                    {{ assessment.confidence|floatformat:1 }}%

                </p>

            </article>


            <article class="decision-card">

                <p class="kicker">
                    WHAT THIS MEANS
                </p>


                <h2>

                    {% if assessment.risk_level == "HIGH" %}

                        Review the plan before departure.

                    {% elif assessment.risk_level == "MEDIUM" %}

                        Travel is possible with preparation.

                    {% else %}

                        Conditions look favourable.

                    {% endif %}

                </h2>


                <p>

                    {% if assessment.risk_level == "HIGH" %}

                        Focus on the strongest risk signals.
                        Consider changing timing, transport
                        or travel conditions.

                    {% elif assessment.risk_level == "MEDIUM" %}

                        Reduce avoidable pressure points,
                        check your transport options
                        and keep flexibility in the itinerary.

                    {% else %}

                        Continue monitoring travel conditions
                        and keep normal contingency plans.

                    {% endif %}

                </p>

            </article>

        </div>


        <section class="panel">

            <div class="section-line">

                <div>

                    <p class="kicker">
                        RISK SIGNALS
                    </p>

                    <h2>
                        What influenced this result
                    </h2>

                    <p>
                        A longer bar means that factor
                        contributed more strongly to the
                        overall travel risk.
                    </p>

                </div>


                <span class="model-pill">

                    Model

                    {% if assessment.model_version %}

                        {{ assessment.model_version.version }}

                    {% else %}

                        —

                    {% endif %}

                </span>

            </div>


            <div class="factor-list">

                {% for factor in assessment.explanation.factors %}

                    <div class="factor">

                        <div class="factor-name">

                            <strong>
                                {{ factor.name }}
                            </strong>

                            <span>
                                {{ factor.value|floatformat:0 }}/100
                            </span>

                        </div>


                        <div class="bar">

                            <i
                                style="width:{{ factor.value }}%"
                            ></i>

                        </div>

                    </div>

                {% empty %}

                    <p>
                        No detailed factor explanation
                        was stored for this assessment.
                    </p>

                {% endfor %}

            </div>

        </section>


        {% if assessment.explanation.probabilities %}

            <section class="panel probability-panel">

                <p class="kicker">
                    MODEL OUTLOOK
                </p>

                <h2>
                    Risk probability distribution
                </h2>


                <div class="probability-grid">

                    {% for label, value in assessment.explanation.probabilities.items %}

                        <div>

                            <span>
                                {{ label|title }}
                            </span>

                            <strong>
                                {{ value|floatformat:1 }}%
                            </strong>

                        </div>

                    {% endfor %}

                </div>

            </section>

        {% endif %}

    </section>

    {% endblock %}
    """
)


# ============================================================
# 11. COMPLETE CSS
# ============================================================

backup_and_write(
    "static/app.css",
    r"""
    :root {
        --ink: #21313b;
        --muted: #65737c;
        --line: #dce3e1;
        --paper: #ffffff;
        --soft: #f4f6f5;
        --deep: #183f3a;
        --deep-light: #28564f;
        --gold: #b68b47;
        --danger: #a94b43;
        --success: #2e6a50;
        --radius: 16px;
        --shadow: 0 10px 28px rgba(20, 40, 42, 0.07);
    }


    * {
        box-sizing: border-box;
    }


    html {
        scroll-behavior: smooth;
    }


    body {
        margin: 0;
        background: #fafbfa;
        color: var(--ink);
        font-family:
            Inter,
            ui-sans-serif,
            system-ui,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
        line-height: 1.6;
    }


    .shell {
        width: min(1080px, calc(100% - 40px));
        margin: auto;
    }


    /* NAVIGATION */

    .topbar {
        background: rgba(255,255,255,.98);
        border-bottom: 1px solid var(--line);
        position: sticky;
        top: 0;
        z-index: 50;
    }


    .nav-shell {
        min-height: 76px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }


    .brand {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        color: var(--ink);
        text-decoration: none;
        font-size: 1.3rem;
        font-weight: 800;
    }


    .brand-badge {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        background: var(--deep);
        color: white;
        font-size: .75rem;
        font-weight: 900;
    }


    .nav-links {
        display: flex;
        align-items: center;
        gap: 7px;
    }


    .nav-links a,
    .nav-signout {
        color: var(--muted);
        background: transparent;
        border: 0;
        padding: 10px 13px;
        border-radius: 9px;
        text-decoration: none;
        font: inherit;
        cursor: pointer;
    }


    .nav-links a:hover,
    .nav-signout:hover {
        color: var(--deep);
        background: var(--soft);
    }


    .nav-cta,
    .nav-signout {
        background: var(--deep) !important;
        color: white !important;
    }


    .logout-form {
        margin: 0;
    }


    .menu-toggle {
        display: none;
        background: white;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 8px 12px;
        cursor: pointer;
    }


    /* BUTTONS */

    .button {
        min-height: 46px;
        padding: 11px 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        border: 1px solid transparent;
        text-decoration: none;
        font-weight: 750;
        cursor: pointer;
        font: inherit;
    }


    .primary {
        background: var(--deep);
        color: white;
    }


    .primary:hover {
        background: var(--deep-light);
    }


    .secondary {
        background: white;
        color: var(--deep);
        border-color: #bcc8c4;
    }


    .light {
        background: white;
        color: var(--deep);
    }


    .full {
        width: 100%;
    }


    /* HERO */

    .hero {
        background: var(--soft);
        padding: 90px 0 75px;
        border-bottom: 1px solid var(--line);
    }


    .hero-grid {
        display: grid;
        grid-template-columns: 1.15fr .85fr;
        gap: 60px;
        align-items: center;
    }


    .kicker {
        margin: 0 0 10px;
        color: #627078;
        font-size: .74rem;
        font-weight: 850;
        letter-spacing: .17em;
    }


    .hero h1 {
        margin: 0 0 22px;
        font-size: clamp(2.8rem, 6vw, 5rem);
        line-height: 1.02;
        letter-spacing: -.045em;
    }


    .lead {
        max-width: 620px;
        color: var(--muted);
        font-size: 1.08rem;
    }


    .hero-actions,
    .result-actions {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 28px;
    }


    .trust-row {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 25px;
        color: var(--muted);
        font-size: .9rem;
    }


    /* SAMPLE CARD */

    .sample-card {
        background: var(--deep);
        color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: var(--shadow);
    }


    .sample-top {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }


    .sample-top span {
        font-size: .72rem;
        font-weight: 850;
        letter-spacing: .14em;
        color: #c8d4d0;
    }


    .sample-score {
        display: flex;
        align-items: flex-end;
        gap: 12px;
        margin: 28px 0;
    }


    .sample-score strong {
        font-size: 4.5rem;
        line-height: .9;
    }


    .sample-score span {
        margin-bottom: 8px;
        color: #c8d4d0;
        font-size: .9rem;
    }


    .signal {
        display: grid;
        grid-template-columns: 70px 1fr 55px;
        align-items: center;
        gap: 10px;
        margin: 14px 0;
        font-size: .84rem;
    }


    .signal div {
        height: 6px;
        background: rgba(255,255,255,.18);
        border-radius: 999px;
        overflow: hidden;
    }


    .signal i {
        display: block;
        height: 100%;
        background: #c5a264;
        border-radius: 999px;
    }


    .sample-note {
        border-top: 1px solid rgba(255,255,255,.16);
        margin: 22px 0 0;
        padding-top: 18px;
        color: #d5dfdc;
        font-size: .9rem;
    }


    /* SECTIONS */

    .section,
    .page-section {
        padding: 72px 0;
    }


    .section-heading {
        max-width: 680px;
        margin-bottom: 34px;
    }


    .section-heading h2,
    .section-line h2,
    .form-heading h2,
    .panel h2 {
        margin: 0 0 10px;
        font-size: clamp(1.7rem, 3vw, 2.3rem);
        line-height: 1.15;
    }


    .section-heading p:last-child,
    .section-line p,
    .form-heading p {
        color: var(--muted);
        margin: 0;
    }


    .feature-grid,
    .risk-grid,
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
    }


    .feature-card,
    .stat-card,
    .panel,
    .assessment-card,
    .auth-card,
    .empty-state,
    .decision-card {
        background: white;
        border: 1px solid var(--line);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
    }


    .feature-card {
        padding: 26px;
    }


    .feature-card h3 {
        margin: 18px 0 7px;
    }


    .feature-card p {
        color: var(--muted);
        margin: 0;
    }


    .feature-card > span {
        color: var(--deep);
        font-weight: 850;
    }


    .muted {
        background: var(--soft);
        border-top: 1px solid var(--line);
        border-bottom: 1px solid var(--line);
    }


    .risk-grid div {
        padding: 18px;
        background: white;
        border: 1px solid var(--line);
        border-radius: 12px;
        font-weight: 650;
    }


    .cta-section {
        background: var(--deep);
        padding: 55px 0;
    }


    .cta-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 30px;
        color: white;
    }


    .cta-box .kicker {
        color: #c9d5d2;
    }


    .cta-box h2 {
        margin: 0;
        max-width: 680px;
        font-size: clamp(1.8rem, 4vw, 3rem);
        line-height: 1.15;
    }


    /* DASHBOARD */

    .page-hero {
        padding: 65px 0 45px;
        background: var(--soft);
        border-bottom: 1px solid var(--line);
    }


    .hero-row,
    .section-line,
    .assessment-intro,
    .result-header {
        display: flex;
        justify-content: space-between;
        gap: 30px;
    }


    .hero-row {
        align-items: flex-end;
    }


    .page-hero h1 {
        margin: 0 0 10px;
        font-size: clamp(2.5rem, 5vw, 4.2rem);
        line-height: 1.05;
    }


    .page-hero p {
        max-width: 650px;
        color: var(--muted);
        margin: 0;
    }


    .stats-grid {
        margin-bottom: 65px;
    }


    .stat-card {
        padding: 25px;
    }


    .stat-card span {
        display: block;
        color: var(--muted);
        font-size: .72rem;
        font-weight: 850;
        letter-spacing: .12em;
    }


    .stat-card strong {
        display: block;
        margin: 8px 0 3px;
        font-size: 2.3rem;
    }


    .stat-card small {
        color: var(--muted);
    }


    .section-line {
        align-items: center;
        margin: 35px 0 20px;
    }


    .section-line a {
        color: var(--deep);
        text-decoration: none;
        font-weight: 750;
    }


    /* TRIP LIST */

    .trip-list,
    .history-table {
        background: white;
        border: 1px solid var(--line);
        border-radius: var(--radius);
        overflow: hidden;
    }


    .trip-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        padding: 19px 22px;
        color: var(--ink);
        text-decoration: none;
        border-bottom: 1px solid var(--line);
    }


    .trip-row:last-child {
        border-bottom: 0;
    }


    .trip-row:hover,
    .table-row:hover {
        background: #f5f7f6;
    }


    .trip-row strong,
    .table-row strong {
        display: block;
    }


    .trip-row small,
    .table-row small {
        color: var(--muted);
    }


    .trip-meta {
        display: flex;
        align-items: center;
        gap: 20px;
    }


    /* RISK BADGES */

    .risk {
        display: inline-flex;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: .74rem;
        font-weight: 850;
        letter-spacing: .05em;
    }


    .risk.low {
        color: #1f6549;
        background: #e8f2ec;
    }


    .risk.medium {
        color: #8a5d13;
        background: #f8efdd;
    }


    .risk.high {
        color: #963d38;
        background: #f7e7e6;
    }


    /* EMPTY */

    .empty-state {
        text-align: center;
        padding: 55px 25px;
    }


    .empty-icon {
        width: 48px;
        height: 48px;
        display: grid;
        place-items: center;
        margin: 0 auto 15px;
        border-radius: 50%;
        background: #edf2f0;
        color: var(--deep);
    }


    .empty-state h3 {
        margin: 0 0 6px;
    }


    .empty-state p {
        max-width: 520px;
        margin: 0 auto 22px;
        color: var(--muted);
    }


    /* ASSESSMENT */

    .assessment-intro {
        align-items: center;
        margin-bottom: 28px;
    }


    .assessment-intro h1 {
        margin: 0 0 10px;
        font-size: clamp(2.3rem, 5vw, 4rem);
        line-height: 1.05;
    }


    .assessment-intro p {
        color: var(--muted);
        max-width: 720px;
    }


    .progress-chip {
        min-width: 145px;
        padding: 13px 16px;
        background: white;
        border: 1px solid var(--line);
        border-radius: 12px;
    }


    .progress-chip b,
    .progress-chip span {
        display: block;
    }


    .progress-chip span {
        font-size: .8rem;
        color: var(--muted);
    }


    .assessment-card {
        padding: 0 38px;
    }


    .form-section {
        display: grid;
        grid-template-columns: 34px 1fr;
        column-gap: 20px;
        padding: 34px 0;
        border-bottom: 1px solid var(--line);
    }


    .section-number {
        width: 34px;
        height: 34px;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: #edf2f0;
        color: var(--deep);
        font-size: .8rem;
        font-weight: 850;
    }


    .form-heading {
        grid-column: 2;
        margin-bottom: 24px;
    }


    .field-grid {
        grid-column: 2;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }


    .field-grid label,
    .auth-form label {
        display: block;
        font-size: .92rem;
        font-weight: 750;
    }


    .field-control {
        width: 100%;
        height: 50px;
        margin-top: 7px;
        padding: 0 14px;
        background: white;
        border: 1px solid #bcc8c5;
        border-radius: 10px;
        color: var(--ink);
        font: inherit;
        outline: none;
    }


    .field-control:focus {
        border-color: var(--deep);
        box-shadow: 0 0 0 3px rgba(24,63,58,.10);
    }


    .field-grid small,
    .auth-form small {
        display: block;
        margin-top: 6px;
        color: var(--muted);
        font-size: .78rem;
        font-weight: 400;
    }


    .field-error {
        display: block;
        margin-top: 5px;
        color: var(--danger);
        font-size: .82rem;
    }


    .form-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        padding: 25px 0;
    }


    .form-actions span {
        display: block;
        color: var(--muted);
        font-size: .88rem;
    }


    /* HISTORY */

    .table-head,
    .table-row {
        display: grid;
        grid-template-columns: 2fr .8fr .8fr .7fr .5fr;
        gap: 15px;
        align-items: center;
        padding: 17px 22px;
    }


    .table-head {
        background: #f5f7f6;
        color: var(--muted);
        font-size: .7rem;
        font-weight: 850;
        letter-spacing: .1em;
    }


    .table-row {
        color: var(--ink);
        text-decoration: none;
        border-top: 1px solid var(--line);
    }


    /* RESULT */

    .result-header {
        align-items: flex-start;
        margin-bottom: 28px;
    }


    .back-link {
        display: inline-block;
        margin-bottom: 18px;
        color: var(--deep);
        text-decoration: none;
        font-weight: 750;
    }


    .result-header h1 {
        margin: 0 0 9px;
        font-size: clamp(2.1rem, 5vw, 3.7rem);
        line-height: 1.05;
    }


    .result-header p {
        color: var(--muted);
        margin: 0;
    }


    .result-grid {
        display: grid;
        grid-template-columns: .7fr 1.3fr;
        gap: 18px;
        margin-bottom: 18px;
    }


    .score-card {
        background: var(--deep);
        color: white;
        padding: 34px;
        border-radius: var(--radius);
    }


    .score-card small {
        color: #c7d3d0;
        font-weight: 850;
        letter-spacing: .12em;
    }


    .score-card > strong {
        display: block;
        margin: 24px 0 15px;
        font-size: 4.4rem;
        line-height: 1;
    }


    .score-card > strong span {
        font-size: 1.1rem;
        color: #c2ceca;
    }


    .score-card p {
        color: #c7d3d0;
    }


    .decision-card {
        padding: 34px;
    }


    .decision-card h2 {
        margin: 15px 0;
        font-size: clamp(1.7rem, 3vw, 2.4rem);
        line-height: 1.2;
    }


    .decision-card p:last-child {
        color: var(--muted);
    }


    .panel {
        padding: 34px;
        margin-top: 18px;
    }


    .model-pill {
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 8px 12px;
        color: var(--muted);
        font-size: .84rem;
    }


    .factor {
        margin-top: 22px;
    }


    .factor-name {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 8px;
    }


    .factor-name span {
        color: var(--muted);
    }


    .bar {
        height: 7px;
        overflow: hidden;
        background: #e1e7e5;
        border-radius: 999px;
    }


    .bar i {
        display: block;
        height: 100%;
        background: var(--deep);
        border-radius: 999px;
    }


    .probability-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-top: 24px;
    }


    .probability-grid div {
        padding: 18px;
        border: 1px solid var(--line);
        border-radius: 12px;
    }


    .probability-grid span {
        display: block;
        color: var(--muted);
        font-size: .8rem;
    }


    .probability-grid strong {
        display: block;
        margin-top: 4px;
        font-size: 1.7rem;
    }


    /* AUTH */

    .auth-page {
        min-height: calc(100vh - 180px);
        display: grid;
        place-items: center;
        padding: 60px 20px;
        background: var(--soft);
    }


    .auth-card {
        width: min(100%, 480px);
        padding: 36px;
    }


    .auth-card h1 {
        margin: 7px 0;
        font-size: 2.2rem;
        line-height: 1.15;
    }


    .muted-text {
        color: var(--muted);
    }


    .auth-form {
        display: grid;
        gap: 17px;
        margin-top: 25px;
    }


    .auth-switch {
        margin: 22px 0 0;
        text-align: center;
        color: var(--muted);
    }


    .auth-switch a {
        color: var(--deep);
        font-weight: 750;
    }


    /* MESSAGES */

    .flash-wrap {
        padding-top: 16px;
    }


    .flash {
        padding: 12px 16px;
        background: white;
        border: 1px solid var(--line);
        border-radius: 10px;
    }


    .flash.error {
        border-color: #e6c3bf;
        color: #8f3933;
    }


    .flash.success {
        border-color: #bed8c8;
        color: #276044;
    }


    /* FOOTER */

    .footer {
        margin-top: 72px;
        background: white;
        border-top: 1px solid var(--line);
    }


    .footer-inner {
        min-height: 105px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        color: var(--muted);
        font-size: .9rem;
    }


    .footer strong {
        display: block;
        color: var(--ink);
    }


    .footer-inner div span {
        display: block;
    }


    /* MOBILE */

    @media (max-width: 760px) {

        .shell {
            width: min(100% - 28px, 1080px);
        }


        .topbar {
            position: relative;
        }


        .menu-toggle {
            display: block;
        }


        .nav-links {
            display: none;
            position: absolute;
            top: 68px;
            left: 14px;
            right: 14px;
            padding: 12px;
            background: white;
            border: 1px solid var(--line);
            border-radius: 12px;
            box-shadow: var(--shadow);
            flex-direction: column;
            align-items: stretch;
        }


        .nav-links.open {
            display: flex;
        }


        .nav-links a,
        .nav-signout {
            display: block;
            width: 100%;
            text-align: left;
        }


        .hero {
            padding: 58px 0;
        }


        .hero-grid,
        .result-grid,
        .feature-grid,
        .risk-grid,
        .stats-grid,
        .probability-grid {
            grid-template-columns: 1fr;
        }


        .section,
        .page-section {
            padding: 48px 0;
        }


        .hero-row,
        .section-line,
        .assessment-intro,
        .result-header,
        .cta-box,
        .form-actions {
            flex-direction: column;
            align-items: flex-start;
        }


        .assessment-card {
            padding: 0 20px;
        }


        .form-section {
            grid-template-columns: 1fr;
        }


        .form-heading,
        .field-grid {
            grid-column: 1;
        }


        .field-grid {
            grid-template-columns: 1fr;
        }


        .section-number {
            margin-bottom: 14px;
        }


        .table-head {
            display: none;
        }


        .table-row {
            grid-template-columns: 1fr 1fr;
            padding: 18px;
        }


        .table-row > div:nth-child(3),
        .table-row > div:nth-child(4) {
            display: none;
        }


        .table-row > div:last-child {
            text-align: right;
        }


        .result-actions {
            width: 100%;
        }


        .result-actions .button {
            flex: 1;
        }


        .trip-row {
            align-items: flex-start;
        }


        .trip-meta {
            flex-direction: column;
            align-items: flex-end;
            gap: 5px;
        }


        .footer-inner {
            min-height: auto;
            padding: 24px 0;
            flex-direction: column;
            align-items: flex-start;
        }

    }
    """
)


# ============================================================
# 12. FIX STATIC URL
# ============================================================

settings_path = ROOT / "config/settings.py"

if settings_path.exists():

    backup_path = BACKUP / "config/settings.py"

    backup_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(
        settings_path,
        backup_path
    )

    settings = settings_path.read_text(
        encoding="utf-8"
    )

    settings = settings.replace(
        'STATIC_URL = "static/"',
        'STATIC_URL = "/static/"'
    )

    if 'LOGIN_URL = "/accounts/login/"' not in settings:

        settings += '''

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"
'''

    settings_path.write_text(
        settings,
        encoding="utf-8"
    )


# ============================================================
# 13. MAKE CELERY OPTIONAL
# ============================================================

config_init = ROOT / "config/__init__.py"

if config_init.exists():

    backup_path = BACKUP / "config/__init__.py"

    backup_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(
        config_init,
        backup_path
    )


    config_init.write_text(
        '''
try:
    from .celery import app as celery_app
except ModuleNotFoundError:
    celery_app = None

__all__ = ("celery_app",)
'''.lstrip(),
        encoding="utf-8"
    )


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 70)
print("TRAVELSHIELD COMPLETE FIX FINISHED")
print("=" * 70)

print()
print("BACKUP CREATED:")
print(BACKUP)

print()
print("FIXED:")
print("✓ Landing page")
print("✓ Sign up")
print("✓ Sign in")
print("✓ Sign out")
print("✓ Dashboard")
print("✓ New trip assessment")
print("✓ Responsive form")
print("✓ Assessment history")
print("✓ Assessment result page")
print("✓ Risk cards")
print("✓ Risk bars")
print("✓ Mobile navigation")
print("✓ Professional CSS")
print("✓ Raw Django form problem")
print("✓ Static CSS URL")
print("✓ Optional Celery import")

print()
print("NOW RUN:")
print()
print(r".venv\Scripts\python.exe manage.py check")
print(r".venv\Scripts\python.exe manage.py migrate")
print(r".venv\Scripts\python.exe manage.py runserver")
print()
print("OPEN:")
print("http://127.0.0.1:8000/")
print()
print("=" * 70)