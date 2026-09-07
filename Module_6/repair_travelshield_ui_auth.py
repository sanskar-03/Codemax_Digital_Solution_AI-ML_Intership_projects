from pathlib import Path
from datetime import datetime
import shutil
import sys


# ============================================================
# TRAVELSHIELD UI + AUTHENTICATION REPAIR
# Creates backup before changing files
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

if not (BASE_DIR / "manage.py").exists():
    print("\nERROR: Run this script from the TravelShield project folder.")
    print("Expected manage.py in the same folder as this script.")
    sys.exit(1)


def backup_file(path: Path, backup_root: Path):
    if not path.exists():
        return

    relative = path.relative_to(BASE_DIR)
    destination = backup_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)


def write_file(relative_path, content, backup_root):
    path = BASE_DIR / relative_path

    backup_file(path, backup_root)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")

    print(f"FIXED: {relative_path}")


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = BASE_DIR / f"backup_before_ui_auth_fix_{timestamp}"
    backup_root.mkdir(exist_ok=True)

    print("\n" + "=" * 65)
    print("TRAVELSHIELD - UI AND AUTHENTICATION REPAIR")
    print("=" * 65)
    print(f"\nProject : {BASE_DIR}")
    print(f"Backup  : {backup_root}\n")

    # ========================================================
    # 1. ACCOUNTS VIEWS
    # ========================================================

    accounts_views = r'''
from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def safe_next_url(request, default="home"):
    next_url = request.POST.get("next") or request.GET.get("next")

    if next_url:
        parsed = urlparse(next_url)

        if not parsed.netloc and next_url.startswith("/"):
            return next_url

    return default


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(
                request,
                "Please enter both your username and password."
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

                return redirect(safe_next_url(request))

            messages.error(
                request,
                "The username or password you entered is incorrect."
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

    form = UserCreationForm(request.POST or None)

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
            "Please correct the highlighted information and try again."
        )

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

    return redirect("home")
'''

    write_file(
        "accounts/views.py",
        accounts_views,
        backup_root
    )

    # ========================================================
    # 2. ACCOUNTS URLS
    # ========================================================

    accounts_urls = r'''
from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
]
'''

    write_file(
        "accounts/urls.py",
        accounts_urls,
        backup_root
    )

    # ========================================================
    # 3. BASE TEMPLATE
    # ========================================================

    base_html = r'''
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

<header class="site-header">
    <div class="container header-inner">

        <a href="{% url 'landing' %}" class="brand">
            TravelShield
        </a>

        <nav class="main-nav">

            {% if user.is_authenticated %}

                <a href="{% url 'home' %}">
                    Dashboard
                </a>

                <a href="{% url 'workspace' %}">
                    New assessment
                </a>

                <a href="{% url 'assessment_history' %}">
                    History
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
                    class="nav-button"
                >
                    Create account
                </a>

            {% endif %}

        </nav>

    </div>
</header>


{% if messages %}

<div class="message-container">

    {% for message in messages %}

        <div class="message message-{{ message.tags }}">
            {{ message }}
        </div>

    {% endfor %}

</div>

{% endif %}


<main>
    {% block content %}
    {% endblock %}
</main>


<footer class="site-footer">

    <div class="container footer-inner">

        <div>
            <strong>TravelShield</strong>
            <p>
                Structured travel risk assessment.
            </p>
        </div>

        <p>
            © {% now "Y" %} TravelShield
        </p>

    </div>

</footer>

</body>
</html>
'''

    write_file(
        "templates/base.html",
        base_html,
        backup_root
    )

    # ========================================================
    # 4. PROFESSIONAL LANDING PAGE
    # ========================================================

    landing_html = r'''
{% extends "base.html" %}

{% block title %}
TravelShield | Travel Risk Assessment
{% endblock %}


{% block content %}

<section class="hero">

    <div class="container hero-grid">

        <div class="hero-content">

            <div class="eyebrow">
                TRAVEL RISK ASSESSMENT
            </div>

            <h1>
                Plan with context,
                <br>
                not assumptions.
            </h1>

            <p class="hero-description">
                TravelShield provides a structured way to assess
                travel conditions using trip information, weather
                exposure, crowd pressure, transport reliability
                and seasonal context.
            </p>

            <div class="hero-actions">

                {% if user.is_authenticated %}

                    <a
                        href="{% url 'workspace' %}"
                        class="button button-primary"
                    >
                        Start an assessment
                    </a>

                {% else %}

                    <a
                        href="{% url 'register' %}"
                        class="button button-primary"
                    >
                        Get started
                    </a>

                    <a
                        href="{% url 'login' %}"
                        class="button button-secondary"
                    >
                        Sign in
                    </a>

                {% endif %}

            </div>

        </div>


        <div class="workflow-card">

            <div class="workflow-label">
                ASSESSMENT WORKFLOW
            </div>

            <div class="workflow-step">
                <span>01</span>
                <div>
                    <strong>Trip information</strong>
                    <p>Define route, duration and travel context.</p>
                </div>
            </div>

            <div class="workflow-step">
                <span>02</span>
                <div>
                    <strong>Risk assessment</strong>
                    <p>Evaluate the factors affecting the journey.</p>
                </div>
            </div>

            <div class="workflow-step">
                <span>03</span>
                <div>
                    <strong>Model evaluation</strong>
                    <p>Generate a structured risk result.</p>
                </div>
            </div>

            <div class="workflow-step">
                <span>04</span>
                <div>
                    <strong>Report and history</strong>
                    <p>Review previous assessments and export results.</p>
                </div>
            </div>

        </div>

    </div>

</section>


<section class="section section-light">

    <div class="container">

        <div class="section-heading">

            <div>
                <div class="eyebrow">
                    BUILT FOR A CLEAR WORKFLOW
                </div>

                <h2>
                    Everything stays connected.
                </h2>
            </div>

            <p>
                Each assessment follows the same structured process,
                making results easier to review and compare.
            </p>

        </div>


        <div class="feature-grid">

            <article class="feature-card">

                <div class="feature-number">
                    01
                </div>

                <h3>
                    Structured assessment
                </h3>

                <p>
                    Capture consistent trip information and
                    relevant risk indicators.
                </p>

            </article>


            <article class="feature-card">

                <div class="feature-number">
                    02
                </div>

                <h3>
                    Versioned model
                </h3>

                <p>
                    Keep track of the model version used for
                    every assessment.
                </p>

            </article>


            <article class="feature-card">

                <div class="feature-number">
                    03
                </div>

                <h3>
                    Reviewable results
                </h3>

                <p>
                    Access assessment history and generate
                    reports when needed.
                </p>

            </article>

        </div>

    </div>

</section>


<section class="section">

    <div class="container process-layout">

        <div>

            <div class="eyebrow">
                HOW IT WORKS
            </div>

            <h2>
                A simple process from trip details to a clear result.
            </h2>

        </div>

        <div class="process-list">

            <div class="process-item">
                <span>1</span>
                <div>
                    <h3>Enter trip details</h3>
                    <p>
                        Add origin, destination, duration and
                        other assessment factors.
                    </p>
                </div>
            </div>

            <div class="process-item">
                <span>2</span>
                <div>
                    <h3>Run the assessment</h3>
                    <p>
                        The application processes the supplied
                        information through the active model.
                    </p>
                </div>
            </div>

            <div class="process-item">
                <span>3</span>
                <div>
                    <h3>Review and export</h3>
                    <p>
                        Examine the result, confidence information
                        and available report output.
                    </p>
                </div>
            </div>

        </div>

    </div>

</section>

{% endblock %}
'''

    write_file(
        "templates/public/landing.html",
        landing_html,
        backup_root
    )

    # ========================================================
    # 5. LOGIN PAGE
    # ========================================================

    login_html = r'''
{% extends "base.html" %}

{% block title %}
Sign in | TravelShield
{% endblock %}


{% block content %}

<section class="auth-page">

    <div class="auth-card">

        <div class="auth-header">

            <div class="eyebrow">
                ACCOUNT ACCESS
            </div>

            <h1>
                Sign in
            </h1>

            <p>
                Access your travel assessments and reports.
            </p>

        </div>


        <form method="post" class="auth-form">

            {% csrf_token %}

            <input
                type="hidden"
                name="next"
                value="{{ next }}"
            >

            <div class="form-group">

                <label for="username">
                    Username
                </label>

                <input
                    id="username"
                    name="username"
                    type="text"
                    autocomplete="username"
                    required
                    autofocus
                >

            </div>


            <div class="form-group">

                <label for="password">
                    Password
                </label>

                <input
                    id="password"
                    name="password"
                    type="password"
                    autocomplete="current-password"
                    required
                >

            </div>


            <button
                type="submit"
                class="button button-primary button-full"
            >
                Sign in
            </button>

        </form>


        <div class="auth-footer">

            <p>
                New to TravelShield?
            </p>

            <a href="{% url 'register' %}">
                Create an account
            </a>

        </div>

    </div>

</section>

{% endblock %}
'''

    write_file(
        "templates/accounts/login.html",
        login_html,
        backup_root
    )

    # ========================================================
    # 6. REGISTER PAGE
    # ========================================================

    register_html = r'''
{% extends "base.html" %}

{% block title %}
Create account | TravelShield
{% endblock %}


{% block content %}

<section class="auth-page">

    <div class="auth-card auth-card-wide">

        <div class="auth-header">

            <div class="eyebrow">
                CREATE ACCOUNT
            </div>

            <h1>
                Get started
            </h1>

            <p>
                Create your account to begin managing travel
                risk assessments.
            </p>

        </div>


        <form method="post" class="auth-form">

            {% csrf_token %}


            <div class="form-group">

                <label for="{{ form.username.id_for_label }}">
                    Username
                </label>

                {{ form.username }}

                {% if form.username.errors %}

                    <div class="field-error">
                        {{ form.username.errors }}
                    </div>

                {% endif %}

                {% if form.username.help_text %}

                    <div class="field-help">
                        {{ form.username.help_text }}
                    </div>

                {% endif %}

            </div>


            <div class="form-group">

                <label for="{{ form.password1.id_for_label }}">
                    Password
                </label>

                {{ form.password1 }}

                {% if form.password1.errors %}

                    <div class="field-error">
                        {{ form.password1.errors }}
                    </div>

                {% endif %}

                {% if form.password1.help_text %}

                    <div class="field-help">
                        {{ form.password1.help_text|safe }}
                    </div>

                {% endif %}

            </div>


            <div class="form-group">

                <label for="{{ form.password2.id_for_label }}">
                    Confirm password
                </label>

                {{ form.password2 }}

                {% if form.password2.errors %}

                    <div class="field-error">
                        {{ form.password2.errors }}
                    </div>

                {% endif %}

            </div>


            {% if form.non_field_errors %}

                <div class="field-error">
                    {{ form.non_field_errors }}
                </div>

            {% endif %}


            <button
                type="submit"
                class="button button-primary button-full"
            >
                Create account
            </button>

        </form>


        <div class="auth-footer">

            <p>
                Already have an account?
            </p>

            <a href="{% url 'login' %}">
                Sign in
            </a>

        </div>

    </div>

</section>

{% endblock %}
'''

    write_file(
        "templates/accounts/register.html",
        register_html,
        backup_root
    )

    # ========================================================
    # 7. ADD LOGIN SETTINGS
    # ========================================================

    settings_path = BASE_DIR / "config/settings.py"

    if settings_path.exists():

        backup_file(settings_path, backup_root)

        settings_content = settings_path.read_text(
            encoding="utf-8"
        )

        required_settings = '''

# Authentication redirects
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"
'''

        # Remove old duplicate settings
        lines = settings_content.splitlines()

        filtered = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("LOGIN_URL ="):
                continue

            if stripped.startswith("LOGIN_REDIRECT_URL ="):
                continue

            if stripped.startswith("LOGOUT_REDIRECT_URL ="):
                continue

            filtered.append(line)

        settings_path.write_text(
            "\n".join(filtered).rstrip()
            + required_settings
            + "\n",
            encoding="utf-8"
        )

        print("FIXED: config/settings.py")

    # ========================================================
    # 8. PROFESSIONAL CSS
    # ========================================================

    app_css = r'''
/* ==========================================================
   TRAVELSHIELD
   Professional application styling
   ========================================================== */

:root {
    --background: #f5f5f2;
    --surface: #ffffff;
    --surface-muted: #ecece7;
    --border: #d8d8d1;

    --text: #1f2933;
    --text-muted: #66717d;

    --dark: #202a28;
    --dark-soft: #2d3835;

    --primary: #355d55;
    --primary-hover: #294a43;

    --danger: #a83f3f;
    --success: #356344;

    --shadow: 0 18px 45px rgba(0, 0, 0, 0.08);

    --radius: 6px;
    --container: 1120px;
}


* {
    box-sizing: border-box;
}


html {
    min-height: 100%;
}


body {
    margin: 0;

    min-height: 100vh;

    display: flex;
    flex-direction: column;

    background: var(--background);

    color: var(--text);

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


main {
    flex: 1;
}


a {
    color: inherit;
    text-decoration: none;
}


.container {
    width: min(
        calc(100% - 48px),
        var(--container)
    );

    margin: 0 auto;
}


/* ==========================================================
   HEADER
   ========================================================== */

.site-header {
    background: rgba(245, 245, 242, 0.96);

    border-bottom: 1px solid var(--border);

    position: sticky;
    top: 0;

    z-index: 50;

    backdrop-filter: blur(10px);
}


.header-inner {
    min-height: 76px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 24px;
}


.brand {
    font-size: 1.45rem;
    font-weight: 750;

    letter-spacing: -0.03em;

    color: var(--text);
}


.main-nav {
    display: flex;
    align-items: center;

    gap: 22px;

    font-size: 0.95rem;
}


.main-nav > a:not(.nav-button) {
    color: var(--text-muted);
}


.main-nav > a:not(.nav-button):hover {
    color: var(--text);
}


.nav-button,
.nav-signout {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    min-height: 42px;

    padding: 0 18px;

    border-radius: 5px;

    background: var(--primary);
    color: #ffffff;

    border: 1px solid var(--primary);

    font: inherit;
    cursor: pointer;
}


.nav-button:hover,
.nav-signout:hover {
    background: var(--primary-hover);
}


.logout-form {
    margin: 0;
}


/* ==========================================================
   MESSAGES
   ========================================================== */

.message-container {
    width: min(
        calc(100% - 48px),
        760px
    );

    margin: 24px auto 0;
}


.message {
    padding: 14px 18px;

    border: 1px solid var(--border);
    border-left-width: 4px;

    background: var(--surface);
}


.message-success {
    border-left-color: var(--success);
}


.message-error {
    border-left-color: var(--danger);
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.button {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-height: 48px;

    padding: 0 22px;

    border-radius: 5px;

    border: 1px solid transparent;

    font-size: 0.96rem;
    font-weight: 650;

    cursor: pointer;

    transition:
        background 0.2s ease,
        border-color 0.2s ease,
        transform 0.2s ease;
}


.button:hover {
    transform: translateY(-1px);
}


.button-primary {
    background: var(--primary);
    color: #ffffff;
}


.button-primary:hover {
    background: var(--primary-hover);
}


.button-secondary {
    background: transparent;

    border-color: var(--border);

    color: var(--text);
}


.button-secondary:hover {
    background: var(--surface-muted);
}


.button-full {
    width: 100%;
}


/* ==========================================================
   LANDING PAGE
   ========================================================== */

.hero {
    padding: 90px 0 72px;
}


.hero-grid {
    display: grid;

    grid-template-columns:
        minmax(0, 1.1fr)
        minmax(360px, 0.72fr);

    align-items: center;

    gap: 72px;
}


.eyebrow {
    margin-bottom: 18px;

    color: var(--text-muted);

    font-size: 0.76rem;
    font-weight: 750;

    letter-spacing: 0.18em;
}


.hero h1 {
    max-width: 760px;

    margin: 0;

    font-size: clamp(
        3rem,
        6vw,
        5.6rem
    );

    line-height: 0.98;

    letter-spacing: -0.06em;

    font-weight: 760;
}


.hero-description {
    max-width: 680px;

    margin: 34px 0;

    color: var(--text-muted);

    font-size: 1.08rem;

    line-height: 1.8;
}


.hero-actions {
    display: flex;
    flex-wrap: wrap;

    gap: 12px;
}


.workflow-card {
    padding: 34px;

    background: var(--dark);

    color: #edf0ed;

    border-radius: 14px;

    box-shadow: var(--shadow);
}


.workflow-label {
    margin-bottom: 28px;

    font-size: 0.78rem;
    font-weight: 750;

    letter-spacing: 0.1em;
}


.workflow-step {
    display: grid;

    grid-template-columns: 34px 1fr;

    gap: 14px;

    padding: 19px 0;

    border-top: 1px solid rgba(255, 255, 255, 0.12);
}


.workflow-step span {
    color: #aeb9b5;

    font-size: 0.82rem;
}


.workflow-step strong {
    display: block;

    margin-bottom: 5px;

    font-size: 1rem;
}


.workflow-step p {
    margin: 0;

    color: #b9c2be;

    font-size: 0.9rem;
}


/* ==========================================================
   SECTIONS
   ========================================================== */

.section {
    padding: 86px 0;
}


.section-light {
    background: var(--surface-muted);

    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
}


.section-heading {
    display: flex;
    justify-content: space-between;

    align-items: end;

    gap: 50px;

    margin-bottom: 42px;
}


.section-heading h2,
.process-layout h2 {
    max-width: 700px;

    margin: 0;

    font-size: clamp(
        2rem,
        4vw,
        3.4rem
    );

    line-height: 1.08;

    letter-spacing: -0.045em;
}


.section-heading > p {
    max-width: 400px;

    margin: 0;

    color: var(--text-muted);
}


.feature-grid {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    border: 1px solid var(--border);

    background: var(--surface);
}


.feature-card {
    padding: 32px;

    min-height: 260px;
}


.feature-card + .feature-card {
    border-left: 1px solid var(--border);
}


.feature-number {
    margin-bottom: 56px;

    color: var(--text-muted);

    font-size: 0.8rem;
    font-weight: 700;
}


.feature-card h3 {
    margin: 0 0 10px;

    font-size: 1.18rem;
}


.feature-card p {
    margin: 0;

    color: var(--text-muted);
}


.process-layout {
    display: grid;

    grid-template-columns:
        0.85fr
        1fr;

    gap: 90px;
}


.process-list {
    border-top: 1px solid var(--border);
}


.process-item {
    display: grid;

    grid-template-columns: 52px 1fr;

    gap: 18px;

    padding: 28px 0;

    border-bottom: 1px solid var(--border);
}


.process-item > span {
    color: var(--text-muted);

    font-weight: 700;
}


.process-item h3 {
    margin: 0 0 7px;
}


.process-item p {
    margin: 0;

    color: var(--text-muted);
}


/* ==========================================================
   AUTHENTICATION
   ========================================================== */

.auth-page {
    min-height: calc(100vh - 150px);

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 72px 24px;
}


.auth-card {
    width: 100%;
    max-width: 480px;

    padding: 44px;

    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 10px;

    box-shadow: var(--shadow);
}


.auth-card-wide {
    max-width: 540px;
}


.auth-header {
    margin-bottom: 34px;
}


.auth-header .eyebrow {
    margin-bottom: 12px;
}


.auth-header h1 {
    margin: 0 0 8px;

    font-size: 2.25rem;

    letter-spacing: -0.045em;
}


.auth-header p {
    margin: 0;

    color: var(--text-muted);
}


.auth-form {
    display: grid;

    gap: 22px;
}


.form-group {
    display: grid;

    gap: 8px;
}


.form-group label {
    font-size: 0.9rem;

    font-weight: 650;
}


.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;

    min-height: 48px;

    padding: 10px 13px;

    border: 1px solid #c9cbc6;

    border-radius: 5px;

    background: #ffffff;

    color: var(--text);

    font: inherit;

    outline: none;
}


.form-group textarea {
    min-height: 120px;
}


.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    border-color: var(--primary);

    box-shadow:
        0 0 0 3px
        rgba(53, 93, 85, 0.12);
}


.field-help {
    color: var(--text-muted);

    font-size: 0.8rem;

    line-height: 1.5;
}


.field-help ul {
    margin: 8px 0 0;

    padding-left: 18px;
}


.field-error {
    color: var(--danger);

    font-size: 0.84rem;
}


.field-error ul {
    margin: 0;

    padding-left: 18px;
}


.auth-footer {
    margin-top: 28px;

    padding-top: 22px;

    border-top: 1px solid var(--border);

    display: flex;
    justify-content: space-between;

    gap: 12px;

    font-size: 0.9rem;
}


.auth-footer p {
    margin: 0;

    color: var(--text-muted);
}


.auth-footer a {
    color: var(--primary);

    font-weight: 650;
}


/* ==========================================================
   GENERIC CONTENT / DJANGO FORMS
   ========================================================== */

.content-shell {
    width: min(
        calc(100% - 48px),
        1120px
    );

    margin: 54px auto;
}


.page-heading {
    margin-bottom: 32px;
}


.page-heading h1 {
    margin: 0 0 8px;

    font-size: 2.3rem;

    letter-spacing: -0.04em;
}


.page-heading p {
    margin: 0;

    color: var(--text-muted);
}


.card {
    padding: 28px;

    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 8px;
}


table {
    width: 100%;

    border-collapse: collapse;
}


th,
td {
    padding: 14px;

    text-align: left;

    border-bottom: 1px solid var(--border);
}


th {
    color: var(--text-muted);

    font-size: 0.78rem;

    text-transform: uppercase;

    letter-spacing: 0.06em;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.site-footer {
    border-top: 1px solid var(--border);

    background: var(--surface);
}


.footer-inner {
    min-height: 110px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 30px;

    color: var(--text-muted);

    font-size: 0.86rem;
}


.footer-inner strong {
    color: var(--text);
}


.footer-inner p {
    margin: 4px 0 0;
}


/* ==========================================================
   RESPONSIVE
   ========================================================== */

@media (max-width: 900px) {

    .hero-grid,
    .process-layout {
        grid-template-columns: 1fr;
    }

    .hero-grid {
        gap: 46px;
    }

    .section-heading {
        align-items: start;
        flex-direction: column;
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .feature-card + .feature-card {
        border-left: 0;
        border-top: 1px solid var(--border);
    }

}


@media (max-width: 680px) {

    .header-inner {
        min-height: auto;

        padding: 18px 0;

        align-items: flex-start;

        flex-direction: column;
    }

    .main-nav {
        width: 100%;

        flex-wrap: wrap;

        gap: 14px;
    }

    .hero {
        padding: 60px 0;
    }

    .hero h1 {
        font-size: 3rem;
    }

    .auth-card {
        padding: 30px 22px;
    }

    .auth-footer,
    .footer-inner {
        align-items: flex-start;

        flex-direction: column;
    }

}
'''

    write_file(
        "static/app.css",
        app_css,
        backup_root
    )

    print("\n" + "=" * 65)
    print("REPAIR COMPLETED SUCCESSFULLY")
    print("=" * 65)

    print("\nBackup created:")
    print(backup_root)

    print("\nNEXT COMMANDS:")
    print()
    print(".venv\\Scripts\\python.exe manage.py check")
    print(".venv\\Scripts\\python.exe manage.py migrate")
    print(".venv\\Scripts\\python.exe manage.py runserver")
    print()
    print("Then open:")
    print("http://127.0.0.1:8000/")
    print()


if __name__ == "__main__":
    main()