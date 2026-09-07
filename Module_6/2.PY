# repair_focusforge_ai_v1.py
#
# AUTOMATED FOCUSFORGE AI WEBAPP REPAIR
# Creates:
#   - Professional AI landing page
#   - Modern sign in / register pages
#   - Responsive workspace
#   - AI-themed CSS
#   - Better project/task forms
#   - Navigation
#   - Dashboard cards
#   - Focus/priority/status UI
#   - Responsive mobile layout
#
# Run:
#   .venv\Scripts\python.exe repair_focusforge_ai_v1.py
#
# Then:
#   .venv\Scripts\python.exe manage.py check
#   .venv\Scripts\python.exe manage.py runserver

from pathlib import Path
from datetime import datetime
import shutil
import textwrap
import re

ROOT = Path.cwd()

if not (ROOT / "manage.py").exists():
    raise SystemExit(
        "\nERROR: Run this script from the FocusForge project folder.\n"
        "Example:\n"
        "cd C:\\AI_PROJECTS\\FINAL_PROJECTS\\focusforge\n"
        ".venv\\Scripts\\python.exe repair_focusforge_ai_v1.py\n"
    )

BACKUP = ROOT / f"backup_before_focusforge_ai_v1_{datetime.now():%Y%m%d_%H%M%S}"
BACKUP.mkdir(exist_ok=True)

print("=" * 72)
print("FOCUSFORGE AI — AUTOMATED WEBAPP REPAIR")
print("=" * 72)
print(f"Project: {ROOT}")
print(f"Backup : {BACKUP}")
print()

# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------

def backup_file(path: Path):
    if path.exists():
        relative = path.relative_to(ROOT)
        destination = BACKUP / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def write_file(relative_path, content):
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_file(path)
    path.write_text(
        textwrap.dedent(content).strip() + "\n",
        encoding="utf-8"
    )
    print(f"[UPDATED] {relative_path}")


def read_file(relative_path):
    path = ROOT / relative_path
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


# ---------------------------------------------------------------------
# FIND EXISTING URL NAMES
# ---------------------------------------------------------------------

url_files = list(ROOT.rglob("urls.py"))
url_text = "\n".join(
    p.read_text(encoding="utf-8", errors="ignore")
    for p in url_files
)

def url_name_exists(name):
    return bool(re.search(
        rf"name\s*=\s*['\"]{re.escape(name)}['\"]",
        url_text
    ))


def smart_url(preferred, fallback):
    if url_name_exists(preferred):
        return "{% url '" + preferred + "' %}"
    return fallback


WORKSPACE_URL = smart_url("workspace", "/workspace/")
LOGIN_URL = smart_url("login", "/accounts/login/")
REGISTER_URL = (
    smart_url("register", "/accounts/register/")
    if url_name_exists("register")
    else smart_url("signup", "/accounts/register/")
)

# ---------------------------------------------------------------------
# BASE TEMPLATE
# ---------------------------------------------------------------------

write_file(
    "templates/base.html",
    r"""
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#0b1020">
        <title>{% block title %}FocusForge AI{% endblock %}</title>
        <link rel="stylesheet" href="{% static 'app.css' %}">
    </head>

    <body>

    <div class="app-shell">

        {% if user.is_authenticated %}
        <header class="topbar">

            <a href="{{ WORKSPACE_URL|default:'/workspace/' }}" class="brand">
                <div class="brand-mark">
                    <span>F</span>
                </div>

                <div class="brand-copy">
                    <strong>FocusForge</strong>
                    <small>AI PRODUCTIVITY</small>
                </div>
            </a>

            <nav class="main-nav">

                <a href="/workspace/"
                   class="{% if request.path == '/workspace/' %}active{% endif %}">
                    Overview
                </a>

                <a href="/workspace/">
                    Workspace
                </a>

                {% if user.is_staff %}
                <a href="/admin/">
                    Administration
                </a>
                {% endif %}

            </nav>

            <div class="nav-actions">

                <div class="user-chip">
                    <div class="avatar">
                        {{ user.username|first|upper }}
                    </div>

                    <div class="user-info">
                        <strong>{{ user.username }}</strong>
                        <small>Workspace member</small>
                    </div>
                </div>

                <a class="btn btn-ghost btn-small"
                   href="/accounts/logout/">
                    Sign out
                </a>

            </div>

        </header>
        {% endif %}


        <main>
            {% block content %}{% endblock %}
        </main>

    </div>

    <script>
    document.addEventListener("DOMContentLoaded", function () {

        const inputs = document.querySelectorAll(
            "input, textarea, select"
        );

        inputs.forEach(function (input) {

            if (
                input.type !== "hidden" &&
                input.type !== "checkbox" &&
                input.type !== "radio" &&
                input.type !== "submit"
            ) {
                input.classList.add("ff-input");
            }

        });

        document.querySelectorAll("textarea").forEach(function (textarea) {
            textarea.classList.add("ff-textarea");
        });

        document.querySelectorAll("select").forEach(function (select) {
            select.classList.add("ff-select");
        });

    });
    </script>

    </body>
    </html>
    """
)

# ---------------------------------------------------------------------
# LANDING PAGE
# ---------------------------------------------------------------------

write_file(
    "templates/public/landing.html",
    r"""
    {% extends "base.html" %}

    {% block title %}FocusForge AI — Work smarter. Finish stronger.{% endblock %}

    {% block content %}

    <div class="landing">

        <header class="landing-nav">

            <a href="/" class="brand">
                <div class="brand-mark">F</div>

                <div class="brand-copy">
                    <strong>FocusForge</strong>
                    <small>AI PRODUCTIVITY</small>
                </div>
            </a>

            <nav class="landing-links">
                <a href="#features">Features</a>
                <a href="#how-it-works">How it works</a>
            </nav>

            <div class="landing-actions">

                {% if user.is_authenticated %}
                    <a href="/workspace/" class="btn btn-primary">
                        Open workspace →
                    </a>
                {% else %}
                    <a href="/accounts/login/" class="btn btn-ghost">
                        Sign in
                    </a>

                    <a href="/accounts/register/" class="btn btn-primary">
                        Start free →
                    </a>
                {% endif %}

            </div>

        </header>


        <section class="hero">

            <div class="hero-copy">

                <div class="eyebrow ai-eyebrow">
                    <span class="pulse-dot"></span>
                    AI-POWERED PRODUCTIVITY
                </div>

                <h1>
                    Turn scattered work
                    <span>into focused progress.</span>
                </h1>

                <p class="hero-text">
                    FocusForge AI helps you organize projects, prioritize
                    important tasks, and build a clearer path from
                    <strong>“What should I do?”</strong>
                    to
                    <strong>“Done.”</strong>
                </p>

                <div class="hero-actions">

                    {% if user.is_authenticated %}
                        <a href="/workspace/" class="btn btn-primary btn-large">
                            Open my workspace →
                        </a>
                    {% else %}
                        <a href="/accounts/register/" class="btn btn-primary btn-large">
                            Create your workspace →
                        </a>

                        <a href="/accounts/login/" class="btn btn-ghost btn-large">
                            Sign in
                        </a>
                    {% endif %}

                </div>

                <div class="hero-proof">
                    <div>
                        <strong>01</strong>
                        <span>Create projects</span>
                    </div>

                    <div>
                        <strong>02</strong>
                        <span>Plan tasks</span>
                    </div>

                    <div>
                        <strong>03</strong>
                        <span>Stay focused</span>
                    </div>
                </div>

            </div>


            <div class="hero-visual">

                <div class="glow glow-one"></div>
                <div class="glow glow-two"></div>

                <div class="ai-window">

                    <div class="window-top">
                        <div>
                            <span class="live-indicator"></span>
                            FOCUSFORGE AI
                        </div>

                        <span class="window-status">
                            ANALYZING WORKSPACE
                        </span>
                    </div>

                    <div class="ai-score">

                        <div>
                            <span class="mini-label">
                                TODAY'S FOCUS SCORE
                            </span>

                            <strong>87<span>/100</span></strong>

                            <p>
                                Your workload is balanced.
                                Finish the highest priority task first.
                            </p>
                        </div>

                        <div class="score-ring">
                            <span>87%</span>
                        </div>

                    </div>

                    <div class="ai-task-list">

                        <div class="ai-task high">
                            <div class="task-icon">01</div>

                            <div>
                                <strong>Complete project proposal</strong>
                                <small>HIGH PRIORITY · 2H EST.</small>
                            </div>

                            <span class="task-state">FOCUS</span>
                        </div>

                        <div class="ai-task">
                            <div class="task-icon">02</div>

                            <div>
                                <strong>Review design feedback</strong>
                                <small>MEDIUM PRIORITY · 45 MIN</small>
                            </div>

                            <span class="task-state">NEXT</span>
                        </div>

                        <div class="ai-task">
                            <div class="task-icon">03</div>

                            <div>
                                <strong>Prepare weekly update</strong>
                                <small>LOW PRIORITY · 30 MIN</small>
                            </div>

                            <span class="task-state">LATER</span>
                        </div>

                    </div>

                    <div class="ai-insight">
                        <span>✦</span>

                        <p>
                            <strong>AI Insight:</strong>
                            You can reduce context switching by completing
                            your first task before opening a new project.
                        </p>
                    </div>

                </div>

            </div>

        </section>


        <section class="simple-section">

            <div class="section-heading">

                <div class="eyebrow">
                    SIMPLE BY DESIGN
                </div>

                <h2>
                    You do not need another complicated productivity tool.
                </h2>

                <p>
                    FocusForge keeps the workflow simple:
                </p>

            </div>


            <div class="simple-flow">

                <div class="flow-card">

                    <div class="flow-number">1</div>

                    <h3>Create a project</h3>

                    <p>
                        Add the goal or area of work you want to manage.
                    </p>

                </div>

                <div class="flow-arrow">→</div>

                <div class="flow-card">

                    <div class="flow-number">2</div>

                    <h3>Add your tasks</h3>

                    <p>
                        Break the work into clear, manageable actions.
                    </p>

                </div>

                <div class="flow-arrow">→</div>

                <div class="flow-card">

                    <div class="flow-number">3</div>

                    <h3>Focus and finish</h3>

                    <p>
                        Use the workspace to see what deserves attention now.
                    </p>

                </div>

            </div>

        </section>


        <section class="feature-section" id="features">

            <div class="section-heading">

                <div class="eyebrow">
                    BUILT FOR CLEAR THINKING
                </div>

                <h2>
                    Everything you need to
                    <span>move work forward.</span>
                </h2>

            </div>


            <div class="feature-grid">

                <article class="feature-card">

                    <div class="feature-icon">◈</div>

                    <h3>Project workspace</h3>

                    <p>
                        Keep related work together instead of losing it
                        across notes and tabs.
                    </p>

                </article>


                <article class="feature-card featured">

                    <div class="feature-badge">
                        AI READY
                    </div>

                    <div class="feature-icon">✦</div>

                    <h3>Smart prioritization</h3>

                    <p>
                        Turn a long task list into a clearer idea of
                        what should be handled first.
                    </p>

                </article>


                <article class="feature-card">

                    <div class="feature-icon">◎</div>

                    <h3>Progress visibility</h3>

                    <p>
                        See your active projects and work without
                        digging through complicated menus.
                    </p>

                </article>

            </div>

        </section>


        <section class="cta-section">

            <div class="cta-box">

                <div class="eyebrow ai-eyebrow">
                    <span class="pulse-dot"></span>
                    READY WHEN YOU ARE
                </div>

                <h2>
                    Stop organizing work forever.
                    <span>Start finishing it.</span>
                </h2>

                <p>
                    Build your workspace and bring clarity to your projects.
                </p>

                {% if user.is_authenticated %}
                    <a href="/workspace/" class="btn btn-primary btn-large">
                        Go to workspace →
                    </a>
                {% else %}
                    <a href="/accounts/register/" class="btn btn-primary btn-large">
                        Get started free →
                    </a>
                {% endif %}

            </div>

        </section>


        <footer class="landing-footer">

            <div class="brand">
                <div class="brand-mark">F</div>

                <div class="brand-copy">
                    <strong>FocusForge</strong>
                    <small>AI PRODUCTIVITY</small>
                </div>
            </div>

            <p>
                © 2026 FocusForge AI · Build focus. Forge progress.
            </p>

        </footer>

    </div>

    {% endblock %}
    """
)

# ---------------------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------------------

write_file(
    "templates/accounts/login.html",
    r"""
    {% extends "base.html" %}

    {% block title %}Sign in — FocusForge AI{% endblock %}

    {% block content %}

    <div class="auth-page">

        <div class="auth-brand-side">

            <a href="/" class="brand">
                <div class="brand-mark">F</div>

                <div class="brand-copy">
                    <strong>FocusForge</strong>
                    <small>AI PRODUCTIVITY</small>
                </div>
            </a>

            <div class="auth-side-content">

                <div class="eyebrow ai-eyebrow">
                    <span class="pulse-dot"></span>
                    YOUR FOCUS SYSTEM
                </div>

                <h1>
                    Less chaos.
                    <span>More progress.</span>
                </h1>

                <p>
                    Manage projects, organize tasks, and create
                    a workspace built for focused execution.
                </p>

                <div class="auth-stat">
                    <strong>01</strong>
                    <span>Organize your work</span>
                </div>

                <div class="auth-stat">
                    <strong>02</strong>
                    <span>Choose what matters</span>
                </div>

                <div class="auth-stat">
                    <strong>03</strong>
                    <span>Make consistent progress</span>
                </div>

            </div>

        </div>


        <div class="auth-form-side">

            <div class="auth-card">

                <div class="auth-card-head">

                    <div class="eyebrow">
                        WELCOME BACK
                    </div>

                    <h2>Sign in to FocusForge.</h2>

                    <p>
                        Continue building momentum.
                    </p>

                </div>


                {% if form.non_field_errors %}
                    <div class="alert alert-error">
                        {{ form.non_field_errors }}
                    </div>
                {% endif %}


                <form method="post" class="modern-form">

                    {% csrf_token %}

                    {% for field in form %}

                    <div class="form-group">

                        <label for="{{ field.id_for_label }}">
                            {{ field.label }}
                        </label>

                        {{ field }}

                        {% if field.errors %}
                            <div class="field-error">
                                {{ field.errors }}
                            </div>
                        {% endif %}

                    </div>

                    {% endfor %}


                    <button type="submit" class="btn btn-primary btn-full">
                        Sign in →
                    </button>

                </form>


                <div class="auth-divider">
                    <span></span>
                    <p>NEW TO FOCUSFORGE?</p>
                    <span></span>
                </div>

                <p class="auth-switch">
                    Create your workspace in a few seconds.
                </p>

                <a href="/accounts/register/"
                   class="btn btn-ghost btn-full">
                    Create an account
                </a>

            </div>

        </div>

    </div>

    {% endblock %}
    """
)

# ---------------------------------------------------------------------
# REGISTER PAGE
# ---------------------------------------------------------------------

write_file(
    "templates/accounts/register.html",
    r"""
    {% extends "base.html" %}

    {% block title %}Create account — FocusForge AI{% endblock %}

    {% block content %}

    <div class="auth-page">

        <div class="auth-brand-side">

            <a href="/" class="brand">
                <div class="brand-mark">F</div>

                <div class="brand-copy">
                    <strong>FocusForge</strong>
                    <small>AI PRODUCTIVITY</small>
                </div>
            </a>

            <div class="auth-side-content">

                <div class="eyebrow ai-eyebrow">
                    <span class="pulse-dot"></span>
                    START YOUR WORKSPACE
                </div>

                <h1>
                    Build a better
                    <span>way to work.</span>
                </h1>

                <p>
                    Create projects, organize tasks and turn
                    scattered work into clear progress.
                </p>

            </div>

        </div>


        <div class="auth-form-side">

            <div class="auth-card">

                <div class="auth-card-head">

                    <div class="eyebrow">
                        CREATE ACCOUNT
                    </div>

                    <h2>Start using FocusForge.</h2>

                    <p>
                        Set up your account and start organizing your work.
                    </p>

                </div>


                <form method="post" class="modern-form">

                    {% csrf_token %}

                    {% for field in form %}

                    <div class="form-group">

                        <label for="{{ field.id_for_label }}">
                            {{ field.label }}
                        </label>

                        {{ field }}

                        {% if field.help_text %}
                            <small class="field-help">
                                {{ field.help_text }}
                            </small>
                        {% endif %}

                        {% if field.errors %}
                            <div class="field-error">
                                {{ field.errors }}
                            </div>
                        {% endif %}

                    </div>

                    {% endfor %}


                    <button type="submit" class="btn btn-primary btn-full">
                        Create my account →
                    </button>

                </form>


                <p class="auth-switch auth-bottom">
                    Already have an account?
                    <a href="/accounts/login/">
                        Sign in
                    </a>
                </p>

            </div>

        </div>

    </div>

    {% endblock %}
    """
)

# ---------------------------------------------------------------------
# WORKSPACE TEMPLATE
# This template intentionally uses generic Django form handling.
# It supports common project/task context variables without requiring
# backend/model changes.
# ---------------------------------------------------------------------

write_file(
    "templates/workspace/workspace.html",
    r"""
    {% extends "base.html" %}

    {% block title %}Workspace — FocusForge AI{% endblock %}

    {% block content %}

    <div class="workspace-page">

        <section class="workspace-hero">

            <div>

                <div class="eyebrow ai-eyebrow">
                    <span class="pulse-dot"></span>
                    OPERATIONS WORKSPACE
                </div>

                <h1>
                    Good {{ greeting|default:"work" }},
                    <span>{{ user.username }}.</span>
                </h1>

                <p>
                    Keep your projects moving. Add the next task,
                    focus on what matters, and make visible progress.
                </p>

            </div>

            <div class="workspace-hero-actions">

                <a href="#create-project"
                   class="btn btn-primary">
                    + New project
                </a>

                <a href="#create-task"
                   class="btn btn-ghost">
                    + Add task
                </a>

            </div>

        </section>


        <section class="stats-grid">

            <article class="stat-card">

                <div class="stat-top">
                    <span>PROJECTS</span>
                    <span class="stat-icon">◈</span>
                </div>

                <strong>{{ projects|length|default:"0" }}</strong>

                <p>Projects in your workspace</p>

            </article>


            <article class="stat-card">

                <div class="stat-top">
                    <span>TASKS</span>
                    <span class="stat-icon">✓</span>
                </div>

                <strong>{{ tasks|length|default:"0" }}</strong>

                <p>Tasks currently being tracked</p>

            </article>


            <article class="stat-card stat-ai">

                <div class="stat-top">
                    <span>FOCUS MODE</span>
                    <span class="stat-icon">✦</span>
                </div>

                <strong>AI</strong>

                <p>Prioritize one important action next</p>

            </article>

        </section>


        <section class="workspace-grid">

            <div class="workspace-main">

                <div class="section-card" id="create-project">

                    <div class="card-heading">

                        <div>
                            <div class="eyebrow">
                                PROJECT SETUP
                            </div>

                            <h2>Create a project</h2>

                            <p>
                                A project is a larger goal or area of work.
                            </p>
                        </div>

                    </div>


                    <form method="post" class="modern-form">

                        {% csrf_token %}

                        {% if project_form %}
                            {% for field in project_form %}

                            <div class="form-group">

                                <label for="{{ field.id_for_label }}">
                                    {{ field.label }}
                                </label>

                                {{ field }}

                                {% if field.help_text %}
                                <small class="field-help">
                                    {{ field.help_text }}
                                </small>
                                {% endif %}

                                {% if field.errors %}
                                <div class="field-error">
                                    {{ field.errors }}
                                </div>
                                {% endif %}

                            </div>

                            {% endfor %}
                        {% endif %}

                        <button class="btn btn-primary"
                                type="submit">
                            Create project →
                        </button>

                    </form>

                </div>


                <div class="section-card" id="create-task">

                    <div class="card-heading">

                        <div>
                            <div class="eyebrow">
                                NEXT ACTION
                            </div>

                            <h2>Create a task</h2>

                            <p>
                                Add a clear action that moves a project forward.
                            </p>
                        </div>

                    </div>


                    <form method="post" class="modern-form">

                        {% csrf_token %}

                        {% if task_form %}
                            {% for field in task_form %}

                            <div class="form-group">

                                <label for="{{ field.id_for_label }}">
                                    {{ field.label }}
                                </label>

                                {{ field }}

                                {% if field.help_text %}
                                <small class="field-help">
                                    {{ field.help_text }}
                                </small>
                                {% endif %}

                                {% if field.errors %}
                                <div class="field-error">
                                    {{ field.errors }}
                                </div>
                                {% endif %}

                            </div>

                            {% endfor %}
                        {% endif %}

                        <button class="btn btn-primary"
                                type="submit">
                            Add task →
                        </button>

                    </form>

                </div>

            </div>


            <aside class="workspace-sidebar">

                <div class="ai-panel">

                    <div class="ai-panel-head">

                        <div>
                            <span class="live-indicator"></span>
                            FOCUSFORGE AI
                        </div>

                        <span>ACTIVE</span>

                    </div>

                    <h3>
                        Your next best move.
                    </h3>

                    <p>
                        Start with one meaningful task. Completing a
                        focused action is better than opening five
                        unfinished ones.
                    </p>

                    <div class="ai-priority">

                        <span>RECOMMENDED FOCUS</span>

                        <strong>
                            Complete your highest-priority task first.
                        </strong>

                    </div>

                </div>


                <div class="section-card compact-card">

                    <div class="card-heading">

                        <div>
                            <div class="eyebrow">
                                QUICK GUIDE
                            </div>

                            <h3>How FocusForge works</h3>
                        </div>

                    </div>

                    <div class="quick-guide">

                        <div>
                            <span>1</span>
                            <p>Create a project</p>
                        </div>

                        <div>
                            <span>2</span>
                            <p>Add clear tasks</p>
                        </div>

                        <div>
                            <span>3</span>
                            <p>Focus on the next action</p>
                        </div>

                    </div>

                </div>

            </aside>

        </section>


        <section class="section-card projects-section">

            <div class="card-heading">

                <div>
                    <div class="eyebrow">
                        YOUR WORK
                    </div>

                    <h2>Projects</h2>

                    <p>
                        Everything currently in your workspace.
                    </p>
                </div>

            </div>


            {% if projects %}

                <div class="project-grid">

                    {% for project in projects %}

                    <article class="project-card">

                        <div class="project-card-top">

                            <span class="project-number">
                                0{{ forloop.counter }}
                            </span>

                            <span class="status-pill">
                                ACTIVE
                            </span>

                        </div>

                        <h3>
                            {{ project.name }}
                        </h3>

                        <p>
                            {{ project.description|default:"No description added yet."|truncatechars:140 }}
                        </p>

                        <div class="project-card-footer">

                            <span>
                                PROJECT
                            </span>

                            <span>
                                →
                            </span>

                        </div>

                    </article>

                    {% endfor %}

                </div>

            {% else %}

                <div class="empty-state">

                    <div class="empty-icon">
                        ✦
                    </div>

                    <h3>
                        Your workspace is ready.
                    </h3>

                    <p>
                        Create your first project to start organizing your work.
                    </p>

                    <a href="#create-project"
                       class="btn btn-primary">
                        Create first project →
                    </a>

                </div>

            {% endif %}

        </section>

    </div>

    {% endblock %}
    """
)

# ---------------------------------------------------------------------
# FALLBACK TEMPLATE LOCATIONS
# Copy workspace template into common possible locations only if needed.
# ---------------------------------------------------------------------

workspace_source = ROOT / "templates/workspace/workspace.html"

for alternative in [
    ROOT / "workspace/templates/workspace/workspace.html",
]:
    if alternative.parent.exists():
        backup_file(alternative)
        alternative.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(workspace_source, alternative)
        print(f"[UPDATED] {alternative.relative_to(ROOT)}")

# ---------------------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------------------

write_file(
    "static/app.css",
    r"""
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f4f7fb;
        --surface: #ffffff;
        --surface-soft: #f8fafc;
        --ink: #172033;
        --muted: #687386;
        --line: #dfe6ee;

        --navy: #0b1020;
        --navy-2: #111a31;

        --teal: #13c6a3;
        --teal-dark: #07967d;
        --teal-soft: #dffbf4;

        --blue: #5b7cfa;
        --purple: #8d6bff;

        --danger: #dc4d62;

        --shadow: 0 20px 60px rgba(20, 31, 53, .10);
        --shadow-soft: 0 10px 35px rgba(20, 31, 53, .07);

        --radius: 22px;
        --radius-sm: 14px;
    }


    * {
        box-sizing: border-box;
    }


    html {
        scroll-behavior: smooth;
    }


    body {
        margin: 0;
        min-height: 100vh;

        background:
            radial-gradient(
                circle at top right,
                rgba(91, 124, 250, .08),
                transparent 28%
            ),
            var(--bg);

        color: var(--ink);

        font-family:
            "Manrope",
            Inter,
            system-ui,
            sans-serif;

        line-height: 1.6;
    }


    a {
        color: inherit;
        text-decoration: none;
    }


    button,
    input,
    textarea,
    select {
        font: inherit;
    }


    /* =========================================================
       GLOBAL LAYOUT
    ========================================================= */

    .app-shell {
        min-height: 100vh;
    }


    main {
        width: 100%;
    }


    .topbar {
        position: sticky;
        top: 0;
        z-index: 100;

        height: 78px;

        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 30px;

        padding: 0 clamp(20px, 5vw, 90px);

        background: rgba(255, 255, 255, .88);

        backdrop-filter: blur(18px);

        border-bottom: 1px solid rgba(223, 230, 238, .9);
    }


    .brand {
        display: inline-flex;
        align-items: center;
        gap: 11px;
    }


    .brand-mark {
        width: 42px;
        height: 42px;

        display: grid;
        place-items: center;

        border-radius: 13px;

        color: white;

        font-size: 14px;
        font-weight: 800;

        background:
            linear-gradient(
                135deg,
                var(--teal),
                var(--blue)
            );

        box-shadow:
            0 10px 25px rgba(19, 198, 163, .22);
    }


    .brand-copy {
        display: grid;
        line-height: 1.1;
    }


    .brand-copy strong {
        font-size: 18px;
        letter-spacing: -.5px;
    }


    .brand-copy small {
        margin-top: 5px;

        color: var(--muted);

        font-family: "DM Mono", monospace;
        font-size: 8px;
        font-weight: 500;

        letter-spacing: .15em;
    }


    .main-nav {
        display: flex;
        align-items: center;
        gap: 8px;
    }


    .main-nav a {
        padding: 10px 14px;

        color: var(--muted);

        font-size: 14px;
        font-weight: 700;

        border-radius: 10px;

        transition: .2s ease;
    }


    .main-nav a:hover,
    .main-nav a.active {
        color: var(--ink);
        background: var(--surface-soft);
    }


    .nav-actions {
        display: flex;
        align-items: center;
        gap: 14px;
    }


    .user-chip {
        display: flex;
        align-items: center;
        gap: 9px;
    }


    .avatar {
        width: 34px;
        height: 34px;

        display: grid;
        place-items: center;

        border-radius: 50%;

        color: white;

        font-size: 12px;
        font-weight: 800;

        background: var(--navy);
    }


    .user-info {
        display: grid;
        line-height: 1.15;
    }


    .user-info strong {
        font-size: 12px;
    }


    .user-info small {
        color: var(--muted);
        font-size: 10px;
    }


    /* =========================================================
       BUTTONS
    ========================================================= */

    .btn {
        min-height: 44px;

        display: inline-flex;
        align-items: center;
        justify-content: center;

        gap: 8px;

        padding: 10px 17px;

        border: 1px solid transparent;
        border-radius: 12px;

        cursor: pointer;

        font-size: 13px;
        font-weight: 800;

        transition:
            transform .2s ease,
            box-shadow .2s ease,
            background .2s ease;
    }


    .btn:hover {
        transform: translateY(-2px);
    }


    .btn-primary {
        color: #06251f;

        background:
            linear-gradient(
                135deg,
                #25dfb9,
                #73e6d1
            );

        box-shadow:
            0 10px 28px rgba(19, 198, 163, .20);
    }


    .btn-primary:hover {
        box-shadow:
            0 16px 35px rgba(19, 198, 163, .30);
    }


    .btn-ghost {
        color: var(--ink);

        border-color: var(--line);

        background: white;
    }


    .btn-ghost:hover {
        border-color: #cbd5e1;
        box-shadow: var(--shadow-soft);
    }


    .btn-small {
        min-height: 38px;
        padding: 8px 13px;
    }


    .btn-large {
        min-height: 52px;
        padding: 13px 22px;
    }


    .btn-full {
        width: 100%;
    }


    /* =========================================================
       TYPOGRAPHY
    ========================================================= */

    h1,
    h2,
    h3,
    p {
        margin-top: 0;
    }


    h1,
    h2,
    h3 {
        letter-spacing: -.04em;
        line-height: 1.08;
    }


    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        color: #64748b;

        font-family: "DM Mono", monospace;
        font-size: 10px;
        font-weight: 500;

        letter-spacing: .16em;
    }


    .ai-eyebrow {
        color: var(--teal-dark);
    }


    .pulse-dot {
        width: 8px;
        height: 8px;

        border-radius: 50%;

        background: var(--teal);

        box-shadow:
            0 0 0 6px rgba(19, 198, 163, .12);

        animation: pulse 2s infinite;
    }


    @keyframes pulse {

        0%, 100% {
            transform: scale(1);
        }

        50% {
            transform: scale(1.35);
        }

    }


    /* =========================================================
       LANDING
    ========================================================= */

    .landing {
        width: 100%;
        overflow: hidden;

        background:
            radial-gradient(
                circle at 85% 10%,
                rgba(19, 198, 163, .09),
                transparent 24%
            ),
            radial-gradient(
                circle at 15% 30%,
                rgba(91, 124, 250, .06),
                transparent 30%
            ),
            var(--bg);
    }


    .landing-nav {
        width: min(1320px, calc(100% - 40px));

        min-height: 84px;

        margin: 0 auto;

        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 20px;
    }


    .landing-links {
        display: flex;
        gap: 25px;
    }


    .landing-links a {
        color: var(--muted);
        font-size: 13px;
        font-weight: 700;
    }


    .landing-actions {
        display: flex;
        align-items: center;
        gap: 10px;
    }


    .hero {
        width: min(1320px, calc(100% - 40px));

        min-height: 720px;

        margin: 0 auto;

        display: grid;
        grid-template-columns: 1.02fr .98fr;

        align-items: center;

        gap: clamp(50px, 8vw, 120px);

        padding:
            clamp(60px, 10vw, 130px)
            0;
    }


    .hero h1 {
        max-width: 760px;

        margin:
            22px 0
            25px;

        font-size:
            clamp(52px, 7vw, 94px);

        font-weight: 800;

        letter-spacing: -.075em;
    }


    .hero h1 span,
    .section-heading h2 span,
    .cta-box h2 span,
    .auth-side-content h1 span,
    .workspace-hero h1 span {
        display: block;

        color: transparent;

        background:
            linear-gradient(
                90deg,
                var(--teal-dark),
                var(--blue)
            );

        background-clip: text;
        -webkit-background-clip: text;
    }


    .hero-text {
        max-width: 650px;

        color: var(--muted);

        font-size: 17px;
        line-height: 1.8;
    }


    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;

        margin-top: 32px;
    }


    .hero-proof {
        display: flex;
        flex-wrap: wrap;
        gap: 30px;

        margin-top: 55px;
    }


    .hero-proof div {
        display: grid;
        gap: 4px;
    }


    .hero-proof strong {
        color: var(--teal-dark);

        font-family: "DM Mono", monospace;
        font-size: 12px;
    }


    .hero-proof span {
        color: var(--muted);
        font-size: 12px;
        font-weight: 700;
    }


    .hero-visual {
        position: relative;
    }


    .glow {
        position: absolute;

        width: 300px;
        height: 300px;

        border-radius: 50%;

        filter: blur(90px);

        opacity: .18;

        pointer-events: none;
    }


    .glow-one {
        top: -70px;
        right: -70px;

        background: var(--teal);
    }


    .glow-two {
        bottom: -60px;
        left: -50px;

        background: var(--blue);
    }


    .ai-window {
        position: relative;

        padding: 24px;

        border: 1px solid rgba(223, 230, 238, .9);
        border-radius: 26px;

        background:
            linear-gradient(
                145deg,
                rgba(255, 255, 255, .96),
                rgba(247, 250, 252, .95)
            );

        box-shadow:
            0 35px 90px rgba(21, 35, 57, .16);
    }


    .window-top,
    .ai-panel-head {
        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 15px;

        color: var(--muted);

        font-family: "DM Mono", monospace;
        font-size: 10px;

        letter-spacing: .08em;
    }


    .window-top > div {
        display: flex;
        align-items: center;
        gap: 8px;

        color: var(--ink);
        font-weight: 700;
    }


    .window-status {
        padding: 6px 9px;

        border-radius: 999px;

        color: var(--teal-dark);

        background: var(--teal-soft);

        font-size: 8px;
    }


    .live-indicator {
        width: 7px;
        height: 7px;

        display: inline-block;

        border-radius: 50%;

        background: var(--teal);
    }


    .ai-score {
        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 30px;

        padding: 34px 0;
    }


    .mini-label {
        color: var(--muted);

        font-family: "DM Mono", monospace;
        font-size: 9px;

        letter-spacing: .13em;
    }


    .ai-score strong {
        display: block;

        margin: 8px 0;

        font-size: 60px;

        letter-spacing: -.07em;
    }


    .ai-score strong span {
        color: var(--muted);
        font-size: 18px;
    }


    .ai-score p {
        max-width: 320px;

        margin: 0;

        color: var(--muted);
        font-size: 12px;
    }


    .score-ring {
        width: 125px;
        height: 125px;

        flex: 0 0 auto;

        display: grid;
        place-items: center;

        border-radius: 50%;

        background:
            conic-gradient(
                var(--teal) 0 87%,
                #e8edf3 87% 100%
            );
    }


    .score-ring::before {
        content: "";

        position: absolute;

        width: 98px;
        height: 98px;

        border-radius: 50%;

        background: white;
    }


    .score-ring span {
        position: relative;
        z-index: 1;

        font-size: 18px;
        font-weight: 800;
    }


    .ai-task-list {
        display: grid;
        gap: 10px;
    }


    .ai-task {
        display: grid;
        grid-template-columns: 42px 1fr auto;

        align-items: center;

        gap: 12px;

        padding: 13px;

        border: 1px solid var(--line);
        border-radius: 15px;

        background: rgba(255,255,255,.72);
    }


    .ai-task.high {
        border-color: rgba(19, 198, 163, .35);
        background: rgba(223, 251, 244, .38);
    }


    .task-icon {
        width: 40px;
        height: 40px;

        display: grid;
        place-items: center;

        border-radius: 11px;

        color: var(--teal-dark);

        background: var(--teal-soft);

        font-family: "DM Mono", monospace;
        font-size: 10px;
        font-weight: 700;
    }


    .ai-task strong {
        display: block;

        font-size: 12px;
    }


    .ai-task small {
        color: var(--muted);

        font-family: "DM Mono", monospace;
        font-size: 8px;
    }


    .task-state {
        color: var(--muted);

        font-family: "DM Mono", monospace;
        font-size: 8px;
        font-weight: 700;
    }


    .ai-insight {
        display: flex;
        gap: 12px;

        margin-top: 18px;
        padding: 15px;

        border-radius: 15px;

        color: #365052;

        background:
            linear-gradient(
                135deg,
                var(--teal-soft),
                #edf4ff
            );
    }


    .ai-insight span {
        color: var(--teal-dark);
        font-size: 18px;
    }


    .ai-insight p {
        margin: 0;
        font-size: 11px;
    }


    .simple-section,
    .feature-section,
    .cta-section {
        width: min(1320px, calc(100% - 40px));

        margin: 0 auto;

        padding: 110px 0;
    }


    .section-heading {
        max-width: 760px;
    }


    .section-heading h2,
    .cta-box h2 {
        margin: 18px 0;

        font-size:
            clamp(34px, 4vw, 58px);

        font-weight: 800;
    }


    .section-heading > p {
        color: var(--muted);
    }


    .simple-flow {
        display: grid;
        grid-template-columns: 1fr auto 1fr auto 1fr;

        align-items: center;

        gap: 20px;

        margin-top: 55px;
    }


    .flow-card {
        min-height: 220px;

        padding: 30px;

        border: 1px solid var(--line);
        border-radius: var(--radius);

        background: var(--surface);

        box-shadow: var(--shadow-soft);
    }


    .flow-number {
        width: 42px;
        height: 42px;

        display: grid;
        place-items: center;

        margin-bottom: 30px;

        border-radius: 12px;

        color: var(--teal-dark);

        background: var(--teal-soft);

        font-family: "DM Mono", monospace;
        font-weight: 700;
    }


    .flow-card h3 {
        font-size: 20px;
    }


    .flow-card p {
        margin-bottom: 0;
        color: var(--muted);
        font-size: 13px;
    }


    .flow-arrow {
        color: var(--teal-dark);
        font-size: 30px;
        font-weight: 300;
    }


    .feature-section {
        padding-top: 20px;
    }


    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);

        gap: 20px;

        margin-top: 50px;
    }


    .feature-card {
        position: relative;

        min-height: 300px;

        padding: 32px;

        border: 1px solid var(--line);
        border-radius: var(--radius);

        background: var(--surface);

        transition:
            transform .25s ease,
            box-shadow .25s ease;
    }


    .feature-card:hover {
        transform: translateY(-7px);
        box-shadow: var(--shadow);
    }


    .feature-card.featured {
        color: white;

        border-color: transparent;

        background:
            linear-gradient(
                145deg,
                var(--navy),
                var(--navy-2)
            );
    }


    .feature-card.featured p {
        color: #b8c2d4;
    }


    .feature-icon {
        width: 50px;
        height: 50px;

        display: grid;
        place-items: center;

        margin-bottom: 50px;

        border-radius: 15px;

        color: var(--teal-dark);

        background: var(--teal-soft);

        font-size: 22px;
    }


    .feature-card h3 {
        font-size: 22px;
    }


    .feature-card p {
        color: var(--muted);
        font-size: 13px;
    }


    .feature-badge {
        position: absolute;
        top: 22px;
        right: 22px;

        padding: 6px 9px;

        border-radius: 999px;

        color: var(--teal);

        background: rgba(19, 198, 163, .12);

        font-family: "DM Mono", monospace;
        font-size: 8px;

        letter-spacing: .1em;
    }


    .cta-section {
        padding-bottom: 70px;
    }


    .cta-box {
        position: relative;

        overflow: hidden;

        padding:
            clamp(45px, 7vw, 90px);

        border-radius: 32px;

        color: white;

        background:
            radial-gradient(
                circle at 80% 20%,
                rgba(19, 198, 163, .25),
                transparent 24%
            ),
            linear-gradient(
                135deg,
                #0b1020,
                #172444
            );
    }


    .cta-box h2 {
        max-width: 850px;
    }


    .cta-box p {
        color: #b8c2d4;
    }


    .landing-footer {
        width: min(1320px, calc(100% - 40px));

        margin: 0 auto;

        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 20px;

        padding: 30px 0 45px;

        border-top: 1px solid var(--line);
    }


    .landing-footer p {
        margin: 0;
        color: var(--muted);
        font-size: 11px;
    }


    /* =========================================================
       AUTH
    ========================================================= */

    .auth-page {
        min-height: 100vh;

        display: grid;
        grid-template-columns: 1fr 1fr;
    }


    .auth-brand-side {
        position: relative;

        min-height: 100vh;

        padding:
            clamp(30px, 5vw, 80px);

        overflow: hidden;

        color: white;

        background:
            radial-gradient(
                circle at 75% 20%,
                rgba(19, 198, 163, .18),
                transparent 26%
            ),
            linear-gradient(
                145deg,
                #0a1020,
                #172440
            );
    }


    .auth-brand-side .brand-copy small {
        color: #8290a8;
    }


    .auth-side-content {
        max-width: 590px;

        margin:
            clamp(100px, 18vh, 190px)
            auto
            0;
    }


    .auth-side-content h1 {
        margin: 20px 0;

        font-size:
            clamp(46px, 5vw, 75px);

        font-weight: 800;
    }


    .auth-side-content p {
        max-width: 540px;

        color: #aab6c9;

        font-size: 16px;
    }


    .auth-stat {
        display: flex;
        align-items: center;
        gap: 15px;

        margin-top: 20px;
    }


    .auth-stat strong {
        width: 34px;

        color: var(--teal);

        font-family: "DM Mono", monospace;
        font-size: 11px;
    }


    .auth-stat span {
        color: #d7dfeb;
        font-size: 13px;
    }


    .auth-form-side {
        display: grid;
        place-items: center;

        padding: 35px;
    }


    .auth-card {
        width: min(100%, 500px);
    }


    .auth-card-head {
        margin-bottom: 35px;
    }


    .auth-card h2 {
        margin: 15px 0 10px;

        font-size: 38px;
    }


    .auth-card-head p,
    .auth-switch {
        color: var(--muted);
        font-size: 13px;
    }


    .auth-divider {
        display: grid;
        grid-template-columns: 1fr auto 1fr;

        align-items: center;

        gap: 10px;

        margin: 28px 0 15px;
    }


    .auth-divider span {
        height: 1px;
        background: var(--line);
    }


    .auth-divider p {
        margin: 0;

        color: #9aa5b5;

        font-family: "DM Mono", monospace;
        font-size: 8px;

        letter-spacing: .1em;
    }


    .auth-bottom {
        margin-top: 24px;
        text-align: center;
    }


    .auth-switch a {
        color: var(--teal-dark);
        font-weight: 800;
    }


    /* =========================================================
       FORMS
    ========================================================= */

    .modern-form {
        display: grid;
        gap: 19px;
    }


    .form-group {
        display: grid;
        gap: 7px;
    }


    .form-group label {
        color: var(--ink);

        font-size: 12px;
        font-weight: 800;
    }


    .ff-input,
    .ff-textarea,
    .ff-select,
    .modern-form input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]),
    .modern-form textarea,
    .modern-form select {
        width: 100%;

        min-height: 48px;

        padding: 12px 14px;

        outline: none;

        border: 1px solid #d7e0ea;
        border-radius: 12px;

        color: var(--ink);

        background: white;

        transition:
            border .2s ease,
            box-shadow .2s ease;
    }


    .ff-textarea,
    .modern-form textarea {
        min-height: 120px;
        resize: vertical;
    }


    .ff-input:focus,
    .ff-textarea:focus,
    .ff-select:focus,
    .modern-form input:focus,
    .modern-form textarea:focus,
    .modern-form select:focus {
        border-color: var(--teal);

        box-shadow:
            0 0 0 4px rgba(19, 198, 163, .11);
    }


    .field-help {
        color: var(--muted);
        font-size: 10px;
    }


    .field-error,
    .errorlist {
        margin: 0;
        padding: 0;

        color: var(--danger);

        font-size: 11px;

        list-style: none;
    }


    .alert {
        margin-bottom: 18px;
        padding: 13px;

        border-radius: 12px;

        font-size: 12px;
    }


    .alert-error {
        color: #9d2639;

        border: 1px solid #ffd4da;

        background: #fff1f3;
    }


    /* =========================================================
       WORKSPACE
    ========================================================= */

    .workspace-page {
        width: min(1320px, calc(100% - 40px));

        margin: 0 auto;

        padding: 75px 0 100px;
    }


    .workspace-hero {
        display: flex;
        align-items: end;
        justify-content: space-between;

        gap: 35px;

        margin-bottom: 45px;
    }


    .workspace-hero h1 {
        max-width: 780px;

        margin:
            16px 0;

        font-size:
            clamp(40px, 5vw, 68px);
    }


    .workspace-hero p {
        max-width: 650px;

        margin: 0;

        color: var(--muted);
        font-size: 14px;
    }


    .workspace-hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }


    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);

        gap: 16px;

        margin-bottom: 24px;
    }


    .stat-card {
        min-height: 180px;

        padding: 25px;

        border: 1px solid var(--line);
        border-radius: var(--radius);

        background: white;

        box-shadow: var(--shadow-soft);
    }


    .stat-ai {
        color: white;

        border-color: transparent;

        background:
            linear-gradient(
                135deg,
                var(--navy),
                #1c3153
            );
    }


    .stat-top {
        display: flex;
        justify-content: space-between;

        color: var(--muted);

        font-family: "DM Mono", monospace;
        font-size: 9px;

        letter-spacing: .12em;
    }


    .stat-ai .stat-top,
    .stat-ai p {
        color: #aebbd0;
    }


    .stat-icon {
        color: var(--teal);
        font-size: 16px;
    }


    .stat-card strong {
        display: block;

        margin: 22px 0 5px;

        font-size: 46px;

        letter-spacing: -.06em;
    }


    .stat-card p {
        margin: 0;
        color: var(--muted);
        font-size: 11px;
    }


    .workspace-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 360px;

        gap: 24px;

        align-items: start;
    }


    .workspace-main {
        display: grid;
        gap: 24px;
    }


    .workspace-sidebar {
        position: sticky;
        top: 100px;

        display: grid;
        gap: 20px;
    }


    .section-card {
        padding:
            clamp(25px, 4vw, 42px);

        border: 1px solid var(--line);
        border-radius: var(--radius);

        background: white;

        box-shadow: var(--shadow-soft);
    }


    .card-heading {
        margin-bottom: 28px;
    }


    .card-heading h2 {
        margin:
            12px 0 8px;

        font-size: 29px;
    }


    .card-heading h3 {
        margin:
            10px 0 0;

        font-size: 20px;
    }


    .card-heading p {
        margin: 0;

        color: var(--muted);
        font-size: 12px;
    }


    .ai-panel {
        padding: 27px;

        border-radius: var(--radius);

        color: white;

        background:
            radial-gradient(
                circle at top right,
                rgba(19, 198, 163, .17),
                transparent 30%
            ),
            linear-gradient(
                145deg,
                #0b1020,
                #15203b
            );

        box-shadow:
            0 25px 55px rgba(10, 16, 32, .2);
    }


    .ai-panel-head {
        color: #b6c3d8;
    }


    .ai-panel-head > div {
        display: flex;
        align-items: center;
        gap: 8px;

        color: white;
    }


    .ai-panel-head > span {
        padding: 5px 7px;

        border-radius: 999px;

        color: var(--teal);

        background: rgba(19, 198, 163, .1);

        font-size: 8px;
    }


    .ai-panel h3 {
        margin:
            30px 0
            12px;

        font-size: 27px;
    }


    .ai-panel p {
        color: #aebbd0;
        font-size: 12px;
    }


    .ai-priority {
        display: grid;
        gap: 7px;

        margin-top: 22px;
        padding: 15px;

        border: 1px solid rgba(255,255,255,.08);
        border-radius: 14px;

        background: rgba(255,255,255,.04);
    }


    .ai-priority span {
        color: var(--teal);

        font-family: "DM Mono", monospace;
        font-size: 8px;

        letter-spacing: .1em;
    }


    .ai-priority strong {
        font-size: 12px;
        line-height: 1.5;
    }


    .compact-card {
        padding: 25px;
    }


    .quick-guide {
        display: grid;
        gap: 16px;
    }


    .quick-guide > div {
        display: flex;
        align-items: center;
        gap: 11px;
    }


    .quick-guide span {
        width: 30px;
        height: 30px;

        display: grid;
        place-items: center;

        border-radius: 9px;

        color: var(--teal-dark);

        background: var(--teal-soft);

        font-family: "DM Mono", monospace;
        font-size: 10px;
    }


    .quick-guide p {
        margin: 0;
        font-size: 12px;
        font-weight: 700;
    }


    .projects-section {
        margin-top: 24px;
    }


    .project-grid {
        display: grid;
        grid-template-columns:
            repeat(auto-fit, minmax(240px, 1fr));

        gap: 16px;
    }


    .project-card {
        min-height: 220px;

        display: flex;
        flex-direction: column;

        padding: 23px;

        border: 1px solid var(--line);
        border-radius: 18px;

        background: var(--surface-soft);

        transition:
            transform .2s ease,
            border .2s ease;
    }


    .project-card:hover {
        transform: translateY(-5px);
        border-color: rgba(19, 198, 163, .5);
    }


    .project-card-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }


    .project-number {
        color: var(--teal-dark);

        font-family: "DM Mono", monospace;
        font-size: 10px;
    }


    .status-pill {
        padding: 5px 8px;

        border-radius: 999px;

        color: var(--teal-dark);

        background: var(--teal-soft);

        font-family: "DM Mono", monospace;
        font-size: 8px;

        letter-spacing: .08em;
    }


    .project-card h3 {
        margin:
            30px 0
            10px;

        font-size: 20px;
    }


    .project-card p {
        color: var(--muted);
        font-size: 11px;
    }


    .project-card-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;

        margin-top: auto;

        padding-top: 20px;

        color: var(--muted);

        font-family: "DM Mono", monospace;
        font-size: 9px;

        letter-spacing: .1em;
    }


    .empty-state {
        min-height: 300px;

        display: grid;
        place-items: center;

        align-content: center;

        text-align: center;
    }


    .empty-icon {
        width: 60px;
        height: 60px;

        display: grid;
        place-items: center;

        margin-bottom: 20px;

        border-radius: 20px;

        color: var(--teal-dark);

        background: var(--teal-soft);

        font-size: 26px;
    }


    .empty-state h3 {
        margin-bottom: 8px;
        font-size: 25px;
    }


    .empty-state p {
        max-width: 390px;

        color: var(--muted);
        font-size: 12px;
    }


    /* =========================================================
       DJANGO DEFAULT CONTENT SAFETY
    ========================================================= */

    form p {
        margin: 0 0 18px;
    }


    form p label {
        display: block;

        margin-bottom: 7px;

        font-size: 12px;
        font-weight: 800;
    }


    form p input,
    form p textarea,
    form p select {
        width: 100%;

        min-height: 46px;

        padding: 11px 13px;

        border: 1px solid #d7e0ea;
        border-radius: 12px;

        background: white;
    }


    /* =========================================================
       RESPONSIVE
    ========================================================= */

    @media (max-width: 1050px) {

        .hero {
            grid-template-columns: 1fr;
        }

        .hero-copy {
            max-width: 850px;
        }

        .workspace-grid {
            grid-template-columns: 1fr;
        }

        .workspace-sidebar {
            position: static;

            grid-template-columns: 1fr 1fr;
        }

        .auth-page {
            grid-template-columns: 1fr;
        }

        .auth-brand-side {
            min-height: auto;
        }

        .auth-side-content {
            margin: 80px 0 20px;
        }

        .auth-form-side {
            min-height: 650px;
        }

    }


    @media (max-width: 760px) {

        .topbar {
            height: auto;

            flex-wrap: wrap;

            padding: 15px 20px;
        }

        .main-nav {
            order: 3;

            width: 100%;

            overflow-x: auto;
        }

        .nav-actions {
            margin-left: auto;
        }

        .user-chip {
            display: none;
        }

        .landing-nav {
            min-height: 72px;
        }

        .landing-links {
            display: none;
        }

        .landing-actions .btn-ghost {
            display: none;
        }

        .hero,
        .simple-section,
        .feature-section,
        .cta-section,
        .workspace-page {
            width: min(100% - 28px, 1320px);
        }

        .hero {
            padding: 70px 0;
        }

        .hero h1 {
            font-size: clamp(48px, 15vw, 74px);
        }

        .ai-score {
            align-items: flex-start;
            flex-direction: column;
        }

        .simple-flow {
            grid-template-columns: 1fr;
        }

        .flow-arrow {
            display: none;
        }

        .feature-grid {
            grid-template-columns: 1fr;
        }

        .landing-footer {
            width: min(100% - 28px, 1320px);

            align-items: flex-start;
            flex-direction: column;
        }

        .workspace-page {
            padding-top: 45px;
        }

        .workspace-hero {
            align-items: flex-start;
            flex-direction: column;
        }

        .stats-grid {
            grid-template-columns: 1fr;
        }

        .workspace-sidebar {
            grid-template-columns: 1fr;
        }

        .auth-brand-side {
            padding: 30px 25px;
        }

        .auth-side-content {
            margin: 70px 0 10px;
        }

        .auth-side-content h1 {
            font-size: 48px;
        }

        .auth-form-side {
            padding: 50px 22px;
        }

        .auth-card h2 {
            font-size: 32px;
        }

    }


    @media (max-width: 480px) {

        .brand-copy strong {
            font-size: 16px;
        }

        .brand-mark {
            width: 38px;
            height: 38px;
        }

        .nav-actions .btn {
            display: none;
        }

        .landing-actions .btn {
            min-height: 40px;
            padding: 8px 12px;
            font-size: 11px;
        }

        .hero-actions {
            display: grid;
        }

        .hero-actions .btn {
            width: 100%;
        }

        .ai-window {
            padding: 16px;
        }

        .ai-task {
            grid-template-columns: 36px 1fr;
        }

        .task-state {
            display: none;
        }

        .workspace-hero-actions {
            width: 100%;
        }

        .workspace-hero-actions .btn {
            flex: 1;
        }

    }
    """
)

# ---------------------------------------------------------------------
# SETTINGS CHECK / STATIC FILE SUPPORT
# ---------------------------------------------------------------------

settings_candidates = [
    ROOT / "config" / "settings.py",
]

for settings_path in settings_candidates:

    if not settings_path.exists():
        continue

    content = settings_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    original = content

    # Ensure STATIC_URL exists.
    if "STATIC_URL" not in content:
        content += "\nSTATIC_URL = 'static/'\n"

    # Ensure static directory is configured safely.
    if "STATICFILES_DIRS" not in content:
        content += (
            "\nSTATICFILES_DIRS = [BASE_DIR / 'static']\n"
        )

    if content != original:
        backup_file(settings_path)
        settings_path.write_text(
            content,
            encoding="utf-8"
        )
        print("[UPDATED] config/settings.py")

# ---------------------------------------------------------------------
# CREATE A SIMPLE HOME URL PATCH ONLY IF ROOT URL HAS NO LANDING ROUTE
# We avoid destructive URL replacement.
# ---------------------------------------------------------------------

config_urls = ROOT / "config" / "urls.py"

if config_urls.exists():

    content = config_urls.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    if "public/landing.html" not in content and "TemplateView" not in content:

        backup_file(config_urls)

        if "from django.urls import" in content:
            content = re.sub(
                r"(from django\.urls import [^\n]+)",
                r"\1\nfrom django.views.generic import TemplateView",
                content,
                count=1
            )

        if "urlpatterns = [" in content:
            content = content.replace(
                "urlpatterns = [",
                """urlpatterns = [
    path("", TemplateView.as_view(template_name="public/landing.html"), name="home"),""",
                1
            )

        config_urls.write_text(
            content,
            encoding="utf-8"
        )

        print("[UPDATED] config/urls.py — added landing page route")

# ---------------------------------------------------------------------
# DONE
# ---------------------------------------------------------------------

print()
print("=" * 72)
print("FOCUSFORGE AI FRONTEND REPAIR COMPLETE")
print("=" * 72)
print()
print(f"Backup created:")
print(f"  {BACKUP}")
print()
print("NEXT COMMANDS:")
print()
print("1. Check Django:")
print("   .venv\\Scripts\\python.exe manage.py check")
print()
print("2. Run server:")
print("   .venv\\Scripts\\python.exe manage.py runserver")
print()
print("3. Open:")
print("   http://127.0.0.1:8000/")
print()
print("4. Then test:")
print("   /")
print("   /accounts/login/")
print("   /accounts/register/")
print("   /workspace/")
print()
print("If static CSS does not update immediately:")
print("   Ctrl + F5")
print()