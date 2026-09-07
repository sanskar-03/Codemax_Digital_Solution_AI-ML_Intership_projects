from pathlib import Path
from datetime import datetime
import shutil
import textwrap


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES = BASE_DIR / "templates"
STATIC = BASE_DIR / "static"

BACKUP_DIR = BASE_DIR / (
    "backup_before_ui_improvement_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
)


def backup_file(path):
    if path.exists():
        relative = path.relative_to(BASE_DIR)
        destination = BACKUP_DIR / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def write_file(path, content):
    backup_file(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        textwrap.dedent(content).strip() + "\n",
        encoding="utf-8"
    )

    print(f"Updated: {path.relative_to(BASE_DIR)}")


print("=" * 70)
print("TRAVELSHIELD UI IMPROVEMENT")
print("=" * 70)

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# BASE TEMPLATE
# ============================================================

write_file(
    TEMPLATES / "base.html",
    r"""
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>
            {% block title %}TravelShield{% endblock %}
        </title>

        <link rel="stylesheet" href="{% static 'app.css' %}">
    </head>

    <body>

        <header class="site-header">
            <div class="nav-container">

                <a href="/" class="brand">
                    <span class="brand-mark">TS</span>
                    <span>TravelShield</span>
                </a>

                <nav class="main-nav">

                    {% if user.is_authenticated %}

                        <a href="/dashboard/">Dashboard</a>
                        <a href="/workspace/">New assessment</a>
                        <a href="/assessments/">History</a>

                        {% if user.is_staff %}
                            <a href="/admin/">Administration</a>
                        {% endif %}

                        <a href="/accounts/logout/" class="nav-button">
                            Sign out
                        </a>

                    {% else %}

                        <a href="/accounts/login/">
                            Sign in
                        </a>

                        <a href="/accounts/register/" class="nav-button">
                            Create account
                        </a>

                    {% endif %}

                </nav>

            </div>
        </header>


        <main class="site-main">

            {% if messages %}

                <div class="messages">

                    {% for message in messages %}
                        <div class="message {{ message.tags }}">
                            {{ message }}
                        </div>
                    {% endfor %}

                </div>

            {% endif %}


            {% block content %}
            {% endblock %}

        </main>


        <footer class="site-footer">

            <div>

                <strong>TravelShield</strong>

                <p>
                    Simple travel risk information for better trip planning.
                </p>

            </div>

            <div>
                © {% now "Y" %} TravelShield
            </div>

        </footer>

    </body>
    </html>
    """
)


# ============================================================
# LANDING PAGE
# ============================================================

write_file(
    TEMPLATES / "public" / "landing.html",
    r"""
    {% extends "base.html" %}

    {% block title %}
    TravelShield | Plan your trip with confidence
    {% endblock %}


    {% block content %}

    <section class="hero">

        <div class="hero-content">

            <p class="eyebrow">
                TRAVEL PLANNING MADE CLEARER
            </p>

            <h1>
                Plan your trip
                <span>with confidence.</span>
            </h1>

            <p class="hero-text">

                TravelShield helps you understand possible weather,
                transport and crowd-related risks before you travel.

            </p>


            <div class="hero-actions">

                {% if user.is_authenticated %}

                    <a href="/workspace/" class="primary-button">
                        Check my trip
                    </a>

                    <a href="/dashboard/" class="secondary-button">
                        View dashboard
                    </a>

                {% else %}

                    <a href="/accounts/register/" class="primary-button">
                        Get started
                    </a>

                    <a href="/accounts/login/" class="secondary-button">
                        Sign in
                    </a>

                {% endif %}

            </div>

        </div>


        <div class="hero-card">

            <div class="trip-preview-header">
                <span>Example trip</span>
                <span class="status status-medium">
                    Moderate
                </span>
            </div>

            <div class="trip-route">

                <div>
                    <small>FROM</small>
                    <strong>Delhi</strong>
                </div>

                <div class="route-arrow">
                    →
                </div>

                <div>
                    <small>TO</small>
                    <strong>Manali</strong>
                </div>

            </div>

            <div class="preview-score">

                <div class="score-circle">
                    52
                </div>

                <div>

                    <strong>Trip risk score</strong>

                    <p>
                        Some conditions may require extra planning.
                    </p>

                </div>

            </div>

        </div>

    </section>


    <section class="how-it-works">

        <div class="section-heading">

            <p class="eyebrow">
                HOW IT WORKS
            </p>

            <h2>
                Three simple steps
            </h2>

        </div>


        <div class="steps-grid">

            <article class="info-card">

                <div class="step-number">
                    1
                </div>

                <h3>
                    Tell us about your trip
                </h3>

                <p>
                    Add your route, travel duration,
                    budget and expected conditions.
                </p>

            </article>


            <article class="info-card">

                <div class="step-number">
                    2
                </div>

                <h3>
                    We assess possible risks
                </h3>

                <p>
                    Your trip information is evaluated
                    using the available risk model.
                </p>

            </article>


            <article class="info-card">

                <div class="step-number">
                    3
                </div>

                <h3>
                    Get a clear recommendation
                </h3>

                <p>
                    See your overall trip score,
                    important risk signals and planning advice.
                </p>

            </article>

        </div>

    </section>


    <section class="feature-section">

        <div>

            <p class="eyebrow">
                WHAT WE CHECK
            </p>

            <h2>
                The important parts of your journey.
            </h2>

        </div>


        <div class="feature-list">

            <div class="feature-item">

                <strong>Weather conditions</strong>

                <p>
                    Understand how expected weather may affect your journey.
                </p>

            </div>


            <div class="feature-item">

                <strong>Destination crowding</strong>

                <p>
                    Consider how busy conditions could affect your experience.
                </p>

            </div>


            <div class="feature-item">

                <strong>Transport reliability</strong>

                <p>
                    Identify possible disruption or uncertainty during travel.
                </p>

            </div>


            <div class="feature-item">

                <strong>Trip context</strong>

                <p>
                    Duration, budget and season are considered as part of the assessment.
                </p>

            </div>

        </div>

    </section>

    {% endblock %}
    """
)


# ============================================================
# DASHBOARD
# ============================================================

write_file(
    TEMPLATES / "workspace" / "dashboard.html",
    r"""
    {% extends "base.html" %}

    {% block title %}
    Dashboard | TravelShield
    {% endblock %}


    {% block content %}

    <section class="page-intro">

        <div>

            <p class="eyebrow">
                YOUR TRAVEL OVERVIEW
            </p>

            <h1>
                Welcome back.
            </h1>

            <p>
                Review your travel assessments or check a new trip.
            </p>

        </div>


        <a href="/workspace/" class="primary-button">
            Check a new trip
        </a>

    </section>


    <section class="stats-grid">

        <div class="stat-card">

            <span>
                Total assessments
            </span>

            <strong>
                {{ total_assessments|default:"0" }}
            </strong>

        </div>


        <div class="stat-card">

            <span>
                Higher-risk trips
            </span>

            <strong>
                {{ high_risk_count|default:"0" }}
            </strong>

        </div>


        <div class="stat-card">

            <span>
                Current model
            </span>

            <strong>
                {{ active_model.version|default:"Not available" }}
            </strong>

        </div>

    </section>


    <section class="content-section">

        <div class="section-header">

            <div>

                <p class="eyebrow">
                    RECENT ACTIVITY
                </p>

                <h2>
                    Recent assessments
                </h2>

            </div>


            <a href="/assessments/" class="text-link">
                View all →
            </a>

        </div>


        {% if recent_assessments %}

            <div class="assessment-list">

                {% for assessment in recent_assessments %}

                    <a
                        href="/assessment/{{ assessment.id }}/"
                        class="assessment-row"
                    >

                        <div>

                            <strong>
                                {{ assessment.origin }}
                                →
                                {{ assessment.destination }}
                            </strong>

                            <span>
                                {{ assessment.duration_days }} days
                            </span>

                        </div>


                        <div class="assessment-risk">

                            <span class="risk-badge risk-{{ assessment.risk_level|lower }}">
                                {{ assessment.risk_level }}
                            </span>

                            <strong>
                                {{ assessment.risk_score|floatformat:0 }}/100
                            </strong>

                        </div>

                    </a>

                {% endfor %}

            </div>

        {% else %}

            <div class="empty-state">

                <h3>
                    No trips checked yet
                </h3>

                <p>
                    Start your first assessment to see travel risk information here.
                </p>

                <a href="/workspace/" class="primary-button">
                    Check my first trip
                </a>

            </div>

        {% endif %}

    </section>

    {% endblock %}
    """
)


# ============================================================
# ASSESSMENT FORM
# ============================================================

write_file(
    TEMPLATES / "workspace" / "assessment_form.html",
    r"""
    {% extends "base.html" %}

    {% block title %}
    Check your trip | TravelShield
    {% endblock %}


    {% block content %}

    <section class="form-page">

        <div class="form-page-header">

            <p class="eyebrow">
                TRIP ASSESSMENT
            </p>

            <h1>
                Tell us about your trip.
            </h1>

            <p>
                Add a few details about your journey.
                We'll turn them into a clear travel risk assessment.
            </p>

        </div>


        <form method="post" class="assessment-form">

            {% csrf_token %}


            <section class="form-section">

                <div class="form-section-heading">

                    <div class="section-count">
                        1
                    </div>

                    <div>

                        <h2>
                            Your trip
                        </h2>

                        <p>
                            Basic information about where and how you are travelling.
                        </p>

                    </div>

                </div>


                <div class="form-grid">

                    <div class="field-group">

                        <label for="{{ form.origin.id_for_label }}">
                            Where are you travelling from?
                        </label>

                        {{ form.origin }}

                        <small>
                            Example: Delhi
                        </small>

                    </div>


                    <div class="field-group">

                        <label for="{{ form.destination.id_for_label }}">
                            Where are you travelling to?
                        </label>

                        {{ form.destination }}

                        <small>
                            Example: Manali
                        </small>

                    </div>


                    <div class="field-group">

                        <label for="{{ form.duration_days.id_for_label }}">
                            How many days is your trip?
                        </label>

                        {{ form.duration_days }}

                        <small>
                            Example: 5
                        </small>

                    </div>


                    <div class="field-group">

                        <label for="{{ form.budget.id_for_label }}">
                            Approximate trip budget
                        </label>

                        {{ form.budget }}

                        <small>
                            Example: 40000
                        </small>

                    </div>

                </div>

            </section>


            <section class="form-section">

                <div class="form-section-heading">

                    <div class="section-count">
                        2
                    </div>

                    <div>

                        <h2>
                            Expected travel conditions
                        </h2>

                        <p>
                            Give a simple estimate based on what you expect during your journey.
                        </p>

                    </div>

                </div>


                <div class="form-grid">

                    <div class="field-group">

                        <label for="{{ form.weather_risk.id_for_label }}">
                            How challenging might the weather be?
                        </label>

                        {{ form.weather_risk }}

                        <small>
                            1 means very low impact. 10 means severe conditions.
                        </small>

                    </div>


                    <div class="field-group">

                        <label for="{{ form.crowd_level.id_for_label }}">
                            How crowded do you expect the destination to be?
                        </label>

                        {{ form.crowd_level }}

                        <small>
                            1 means quiet. 10 means extremely crowded.
                        </small>

                    </div>


                    <div class="field-group">

                        <label for="{{ form.transport_reliability.id_for_label }}">
                            How reliable is your transportation?
                        </label>

                        {{ form.transport_reliability }}

                        <small>
                            Use 1 for poor reliability and 10 for very reliable transport.
                        </small>

                    </div>


                    <div class="field-group">

                        <label for="{{ form.season.id_for_label }}">
                            When are you travelling?
                        </label>

                        {{ form.season }}

                        <small>
                            Choose the season that best matches your trip.
                        </small>

                    </div>

                </div>

            </section>


            {% if form.errors %}

                <div class="form-errors">

                    <strong>
                        Please correct the highlighted information.
                    </strong>

                    {{ form.errors }}

                </div>

            {% endif %}


            <div class="form-actions">

                <a href="/dashboard/" class="secondary-button">
                    Cancel
                </a>

                <button type="submit" class="primary-button">
                    Check my trip
                </button>

            </div>

        </form>

    </section>

    {% endblock %}
    """
)


# ============================================================
# MAIN CSS
# ============================================================

write_file(
    STATIC / "app.css",
    r"""
    * {
        box-sizing: border-box;
    }


    :root {

        --bg: #f6f7f5;
        --surface: #ffffff;
        --surface-soft: #f0f2ef;

        --text: #1f2933;
        --muted: #68737d;

        --border: #dfe4df;

        --primary: #294f48;
        --primary-dark: #1f3d38;

        --low: #347a57;
        --medium: #9a6b24;
        --high: #a7473d;

        --shadow: 0 12px 35px rgba(31, 41, 51, 0.07);

    }


    html {
        scroll-behavior: smooth;
    }


    body {

        margin: 0;

        background: var(--bg);

        color: var(--text);

        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;

        line-height: 1.6;

    }


    a {
        color: inherit;
        text-decoration: none;
    }


    /* HEADER */

    .site-header {

        background: rgba(255, 255, 255, 0.94);

        border-bottom: 1px solid var(--border);

        position: sticky;

        top: 0;

        z-index: 20;

    }


    .nav-container {

        max-width: 1180px;

        margin: auto;

        padding: 18px 28px;

        display: flex;

        justify-content: space-between;

        align-items: center;

    }


    .brand {

        display: flex;

        align-items: center;

        gap: 10px;

        font-size: 22px;

        font-weight: 750;

        letter-spacing: -0.5px;

    }


    .brand-mark {

        width: 34px;

        height: 34px;

        border-radius: 9px;

        display: grid;

        place-items: center;

        background: var(--primary);

        color: white;

        font-size: 12px;

        font-weight: 800;

    }


    .main-nav {

        display: flex;

        align-items: center;

        gap: 26px;

        color: var(--muted);

    }


    .main-nav a:hover {
        color: var(--text);
    }


    .nav-button {

        background: var(--primary);

        color: white !important;

        padding: 10px 17px;

        border-radius: 8px;

    }


    /* MAIN */

    .site-main {

        max-width: 1180px;

        margin: auto;

        min-height: calc(100vh - 150px);

        padding: 55px 28px 80px;

    }


    /* BUTTONS */

    .primary-button {

        display: inline-flex;

        align-items: center;

        justify-content: center;

        padding: 13px 22px;

        border-radius: 9px;

        border: 1px solid var(--primary);

        background: var(--primary);

        color: white;

        font-weight: 650;

        cursor: pointer;

        transition: 0.2s ease;

    }


    .primary-button:hover {

        background: var(--primary-dark);

        transform: translateY(-1px);

    }


    .secondary-button {

        display: inline-flex;

        align-items: center;

        justify-content: center;

        padding: 13px 22px;

        border-radius: 9px;

        border: 1px solid var(--border);

        background: white;

        color: var(--text);

        font-weight: 600;

    }


    /* HERO */

    .hero {

        display: grid;

        grid-template-columns: 1.2fr 0.8fr;

        gap: 70px;

        align-items: center;

        min-height: 600px;

    }


    .eyebrow {

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 2px;

        color: #58706a;

        margin-bottom: 16px;

    }


    .hero h1,
    .page-intro h1,
    .form-page-header h1 {

        font-size: clamp(42px, 6vw, 76px);

        line-height: 1.02;

        letter-spacing: -3px;

        margin: 0 0 25px;

    }


    .hero h1 span {
        display: block;
    }


    .hero-text {

        max-width: 650px;

        font-size: 19px;

        color: var(--muted);

    }


    .hero-actions {

        display: flex;

        gap: 12px;

        margin-top: 32px;

    }


    .hero-card {

        background: #20312d;

        color: white;

        padding: 34px;

        border-radius: 18px;

        box-shadow: var(--shadow);

    }


    .trip-preview-header {

        display: flex;

        justify-content: space-between;

        align-items: center;

        color: #d8e0dc;

        font-size: 14px;

    }


    .trip-route {

        display: grid;

        grid-template-columns: 1fr auto 1fr;

        align-items: center;

        gap: 20px;

        margin: 50px 0;

    }


    .trip-route small {

        display: block;

        color: #9daaa6;

        margin-bottom: 5px;

    }


    .trip-route strong {
        font-size: 27px;
    }


    .route-arrow {
        color: #b6c4c0;
        font-size: 26px;
    }


    .preview-score {

        border-top: 1px solid rgba(255,255,255,0.15);

        padding-top: 25px;

        display: flex;

        gap: 20px;

        align-items: center;

    }


    .preview-score p {

        margin: 4px 0 0;

        color: #b9c5c1;

        font-size: 14px;

    }


    .score-circle {

        width: 65px;

        height: 65px;

        border-radius: 50%;

        background: #f0f2ef;

        color: var(--primary);

        display: grid;

        place-items: center;

        font-size: 22px;

        font-weight: 800;

    }


    /* SECTIONS */

    .how-it-works,
    .feature-section,
    .content-section {

        margin-top: 100px;

    }


    .section-heading h2,
    .section-header h2 {

        font-size: 36px;

        margin-top: 0;

        letter-spacing: -1px;

    }


    .steps-grid {

        display: grid;

        grid-template-columns: repeat(3, 1fr);

        gap: 20px;

        margin-top: 35px;

    }


    .info-card {

        background: var(--surface);

        border: 1px solid var(--border);

        border-radius: 14px;

        padding: 30px;

    }


    .info-card h3 {

        font-size: 20px;

        margin: 20px 0 8px;

    }


    .info-card p {
        color: var(--muted);
    }


    .step-number,
    .section-count {

        width: 42px;

        height: 42px;

        border-radius: 50%;

        background: var(--surface-soft);

        color: var(--primary);

        display: grid;

        place-items: center;

        font-size: 14px;

        font-weight: 800;

    }


    .feature-section {

        display: grid;

        grid-template-columns: 0.8fr 1.2fr;

        gap: 70px;

        padding: 55px;

        background: white;

        border: 1px solid var(--border);

        border-radius: 18px;

    }


    .feature-section h2 {

        font-size: 42px;

        line-height: 1.15;

        letter-spacing: -1.5px;

    }


    .feature-list {

        display: grid;

        grid-template-columns: repeat(2, 1fr);

        gap: 15px;

    }


    .feature-item {

        border: 1px solid var(--border);

        border-radius: 12px;

        padding: 22px;

    }


    .feature-item p {

        color: var(--muted);

        margin-bottom: 0;

        font-size: 14px;

    }


    /* DASHBOARD */

    .page-intro {

        display: flex;

        align-items: end;

        justify-content: space-between;

        gap: 30px;

    }


    .page-intro h1 {

        font-size: 56px;

        margin-bottom: 10px;

    }


    .page-intro p {
        color: var(--muted);
    }


    .stats-grid {

        display: grid;

        grid-template-columns: repeat(3, 1fr);

        gap: 18px;

        margin-top: 55px;

    }


    .stat-card {

        background: white;

        border: 1px solid var(--border);

        border-radius: 14px;

        padding: 25px;

    }


    .stat-card span {

        display: block;

        color: var(--muted);

        font-size: 14px;

    }


    .stat-card strong {

        display: block;

        font-size: 32px;

        margin-top: 8px;

    }


    .section-header {

        display: flex;

        align-items: center;

        justify-content: space-between;

    }


    .text-link {

        color: var(--primary);

        font-weight: 700;

    }


    .assessment-list {

        background: white;

        border: 1px solid var(--border);

        border-radius: 14px;

        overflow: hidden;

    }


    .assessment-row {

        padding: 20px 25px;

        display: flex;

        align-items: center;

        justify-content: space-between;

        border-bottom: 1px solid var(--border);

    }


    .assessment-row:last-child {
        border-bottom: none;
    }


    .assessment-row span {

        display: block;

        color: var(--muted);

        font-size: 14px;

        margin-top: 3px;

    }


    .assessment-risk {

        display: flex;

        align-items: center;

        gap: 20px;

    }


    .risk-badge,
    .status {

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 0.5px;

        padding: 6px 10px;

        border-radius: 100px;

    }


    .risk-low {
        background: #e6f1ea;
        color: var(--low);
    }


    .risk-medium,
    .status-medium {
        background: #f5eddb;
        color: var(--medium);
    }


    .risk-high {
        background: #f6e5e3;
        color: var(--high);
    }


    /* FORM */

    .form-page {

        max-width: 1000px;

        margin: auto;

    }


    .form-page-header {

        margin-bottom: 45px;

    }


    .form-page-header h1 {

        font-size: 58px;

        margin-bottom: 15px;

    }


    .form-page-header p {

        color: var(--muted);

        font-size: 18px;

    }


    .assessment-form {

        background: white;

        border: 1px solid var(--border);

        border-radius: 18px;

        padding: 40px;

        box-shadow: var(--shadow);

    }


    .form-section {

        padding-bottom: 38px;

        margin-bottom: 38px;

        border-bottom: 1px solid var(--border);

    }


    .form-section:last-of-type {
        border-bottom: none;
    }


    .form-section-heading {

        display: flex;

        gap: 16px;

        align-items: flex-start;

        margin-bottom: 30px;

    }


    .form-section-heading h2 {

        margin: 0;

        font-size: 25px;

    }


    .form-section-heading p {

        margin: 4px 0 0;

        color: var(--muted);

    }


    .form-grid {

        display: grid;

        grid-template-columns: repeat(2, 1fr);

        gap: 24px;

    }


    .field-group {

        display: flex;

        flex-direction: column;

        gap: 8px;

    }


    .field-group label {

        font-weight: 700;

        font-size: 14px;

    }


    .field-group input,
    .field-group select,
    .field-group textarea {

        width: 100%;

        padding: 14px 15px;

        border-radius: 9px;

        border: 1px solid #cbd3cf;

        background: #fff;

        font-size: 16px;

        font-family: inherit;

        color: var(--text);

    }


    .field-group input:focus,
    .field-group select:focus {

        outline: none;

        border-color: var(--primary);

        box-shadow: 0 0 0 3px rgba(41,79,72,0.10);

    }


    .field-group small {

        color: var(--muted);

        font-size: 12px;

    }


    .form-actions {

        display: flex;

        justify-content: flex-end;

        gap: 12px;

        margin-top: 10px;

    }


    .form-errors {

        background: #f8e9e7;

        color: #7d3028;

        padding: 18px;

        border-radius: 10px;

        margin-bottom: 25px;

    }


    /* EMPTY */

    .empty-state {

        background: white;

        border: 1px dashed #c9d0cc;

        border-radius: 15px;

        padding: 60px 30px;

        text-align: center;

    }


    .empty-state h3 {
        font-size: 24px;
    }


    .empty-state p {

        color: var(--muted);

        margin-bottom: 25px;

    }


    /* MESSAGES */

    .messages {

        max-width: 1180px;

        margin: 0 auto 20px;

    }


    .message {

        padding: 14px 18px;

        border-radius: 9px;

        background: white;

        border: 1px solid var(--border);

    }


    /* FOOTER */

    .site-footer {

        max-width: 1180px;

        margin: auto;

        padding: 35px 28px;

        border-top: 1px solid var(--border);

        display: flex;

        justify-content: space-between;

        color: var(--muted);

        font-size: 14px;

    }


    .site-footer p {

        margin: 5px 0 0;

    }


    /* RESPONSIVE */

    @media (max-width: 850px) {

        .hero,
        .feature-section {

            grid-template-columns: 1fr;

            gap: 40px;

        }


        .steps-grid,
        .stats-grid {

            grid-template-columns: 1fr;

        }


        .form-grid,
        .feature-list {

            grid-template-columns: 1fr;

        }


        .main-nav {

            gap: 12px;

            font-size: 14px;

        }


        .nav-container {

            padding: 14px 18px;

        }


        .site-main {

            padding: 35px 18px 60px;

        }


        .hero {

            min-height: auto;

        }


        .hero h1,
        .form-page-header h1 {

            font-size: 45px;

            letter-spacing: -2px;

        }


        .page-intro {

            align-items: flex-start;

            flex-direction: column;

        }


        .assessment-form {

            padding: 25px 20px;

        }


        .site-footer {

            flex-direction: column;

            gap: 20px;

        }

    }
    """
)


print()
print("=" * 70)
print("UI IMPROVEMENT COMPLETED")
print("=" * 70)
print(f"Backup created: {BACKUP_DIR}")
print()
print("Updated:")
print("  templates/base.html")
print("  templates/public/landing.html")
print("  templates/workspace/dashboard.html")
print("  templates/workspace/assessment_form.html")
print("  static/app.css")
print()
print("NEXT STEP:")
print("  .venv\\Scripts\\python.exe manage.py check")
print("  .venv\\Scripts\\python.exe manage.py runserver")