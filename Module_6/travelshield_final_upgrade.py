from pathlib import Path
from datetime import datetime
import shutil, re, sys

ROOT = Path(__file__).resolve().parent
BACKUP = ROOT.parent / ("travelshield_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S"))

def put(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip()+"\n", encoding="utf-8")
    print("OK:", rel)

def backup():
    BACKUP.mkdir()
    for x in ROOT.iterdir():
        if x.name in {".venv", "__pycache__", ".git"}: continue
        d = BACKUP/x.name
        if x.is_dir(): shutil.copytree(x, d, ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
        else: shutil.copy2(x,d)
    print("Backup:", BACKUP)

def patch_settings():
    p=ROOT/"config/settings.py"; t=p.read_text(encoding="utf-8")
    if "'DIRS': []" in t: t=t.replace("'DIRS': []", "'DIRS': [BASE_DIR / 'templates']")
    if '"DIRS": []' in t: t=t.replace('"DIRS": []', '"DIRS": [BASE_DIR / "templates"]')
    for k,v in {"LOGIN_REDIRECT_URL":"/dashboard/","LOGOUT_REDIRECT_URL":"/"}.items():
        if re.search(rf"^{k}\s*=.*$",t,re.M): t=re.sub(rf"^{k}\s*=.*$",f'{k} = "{v}"',t,flags=re.M)
        else: t+=f'\n{k} = "{v}"\n'
    p.write_text(t,encoding="utf-8"); print("OK: config/settings.py")

def patch_views():
    p=ROOT/"workspace/views.py"; t=p.read_text(encoding="utf-8")
    if "def landing(request):" not in t:
        t += """

def landing(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "public/landing.html")
"""
    if "def assessment_history(request):" not in t:
        t += """

@login_required
def assessment_history(request):
    assessments = TravelAssessment.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "workspace/history.html", {"assessments": assessments})
"""
    p.write_text(t,encoding="utf-8"); print("OK: workspace/views.py")

def predictor():
    put("ml_engine/predictor.py", """
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from workspace.models import RiskModelVersion

SEASON_RISK={"winter":25,"spring":20,"summer":50,"monsoon":80}

def build_feature_row(a):
    weather=float(a.weather_risk)*10
    crowd=float(a.crowd_level)*10
    reliability=float(a.transport_reliability)*10
    duration=float(a.duration_days)
    season=SEASON_RISK.get(str(a.season).lower(),35)
    budget=min(float(a.budget)/250000*100,100)
    return {
        "weather_risk":weather,
        "crime_risk":min(100,crowd*.45+(100-reliability)*.55),
        "health_risk":min(100,weather*.55+duration*1.5),
        "political_risk":min(100,18+season*.35),
        "transport_disruption":min(100,(100-reliability)*.75+weather*.25),
        "destination_popularity":min(100,crowd*.75+budget*.10),
        "trip_duration":duration,
        "season_risk":season,
    }

def predict(assessment):
    mv=RiskModelVersion.objects.filter(active=True).first()
    if not mv: raise RuntimeError("No active risk model is configured.")
    path=Path(mv.artifact_path)
    if not path.is_absolute(): path=Path(__file__).resolve().parent.parent/path
    if not path.exists(): raise RuntimeError(f"Model artifact not found: {path}")
    package=joblib.load(path)
    model=package["model"] if isinstance(package,dict) and "model" in package else package
    columns=package.get("feature_columns") if isinstance(package,dict) else None
    row=build_feature_row(assessment)
    data=pd.DataFrame([[row[c] for c in columns]],columns=columns) if columns else pd.DataFrame([row])
    probs=model.predict_proba(data)[0]
    pm={label:float(value) for label,value in zip(model.classes_,probs)}
    predicted=max(pm,key=pm.get)
    levels={0:"LOW",1:"MEDIUM",2:"HIGH"}
    level=levels.get(int(predicted),"MEDIUM") if isinstance(predicted,(int,np.integer)) else str(predicted).upper()
    weights={0:15,1:55,2:88,"LOW":15,"MEDIUM":55,"HIGH":88}
    score=sum(prob*weights.get(label,50) for label,prob in pm.items())
    named={}
    for key,val in pm.items():
        label=levels.get(int(key),str(key)) if isinstance(key,(int,np.integer)) else str(key).upper()
        named[label]=round(val*100,2)
    factors=[
        ("Weather exposure",row["weather_risk"]),
        ("Transport disruption",row["transport_disruption"]),
        ("Crowd pressure",float(assessment.crowd_level)*10),
        ("Seasonal conditions",row["season_risk"]),
        ("Trip duration",min(100,float(assessment.duration_days)/30*100)),
    ]
    factors.sort(key=lambda x:x[1],reverse=True)
    return {
        "model":mv,"level":level,"score":round(float(score),2),
        "confidence":round(max(pm.values())*100,2),
        "explanation":{"method":"Model probability with trip-context feature mapping",
        "factors":[{"name":n,"value":round(float(v),1)} for n,v in factors],
        "probabilities":named}
    }
""")

def urls():
    put("workspace/urls.py", """
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
""")

def templates():
    put("templates/base.html", """
{% load static %}
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{% block title %}TravelShield{% endblock %}</title><link rel="stylesheet" href="{% static 'app.css' %}"></head>
<body class="{% if user.is_authenticated %}app{% else %}public{% endif %}">
{% if user.is_authenticated %}<aside class="sidebar"><a class="brand" href="{% url 'home' %}">TravelShield<small>TRAVEL RISK INTELLIGENCE</small></a><nav>
<a href="{% url 'home' %}">Dashboard</a><a href="{% url 'workspace' %}">New assessment</a><a href="{% url 'assessment_history' %}">Assessment history</a><a href="{% url 'api_assessments' %}">REST API</a>
{% if user.is_staff %}<a href="/admin/">Administration</a>{% endif %}<a href="{% url 'logout' %}">Sign out</a></nav></aside>{% endif %}
<main>{% block content %}{% endblock %}</main></body></html>
""")
    put("templates/public/landing.html", """
{% extends "base.html" %}{% block title %}TravelShield | Travel Risk Intelligence{% endblock %}{% block content %}
<section class="landing"><header><strong>TravelShield</strong><span><a href="{% url 'login' %}">Sign in</a> <a class="btn" href="{% url 'register' %}">Create account</a></span></header>
<div class="hero"><div><p class="eyebrow">TRAVEL RISK INTELLIGENCE</p><h1>Plan with context, not assumptions.</h1><p>Evaluate weather exposure, crowd pressure, transport reliability, trip duration and seasonal conditions through a structured travel risk workflow.</p><a class="btn" href="{% url 'register' %}">Start an assessment</a></div>
<div class="workflow"><b>ASSESSMENT WORKFLOW</b><p>Trip information</p><i>↓</i><p>Feature mapping</p><i>↓</i><p>Versioned risk model</p><i>↓</i><p>Assessment and report</p></div></div>
<div class="features"><article><b>01</b><h3>Structured assessment</h3><p>Capture trip context consistently.</p></article><article><b>02</b><h3>Versioned model</h3><p>Track the model used for each result.</p></article><article><b>03</b><h3>Exportable result</h3><p>Review history and generate reports.</p></article></div></section>{% endblock %}
""")
    put("templates/workspace/history.html", """
{% extends "base.html" %}{% block content %}<section class="page"><p class="eyebrow">ASSESSMENTS</p><h1>Assessment history</h1><a class="btn" href="{% url 'workspace' %}">New assessment</a>
<div class="card">{% if assessments %}<table><tr><th>Route</th><th>Risk</th><th>Confidence</th><th>Model</th><th></th></tr>{% for a in assessments %}<tr><td>{{ a.origin }} → {{ a.destination }}</td><td>{{ a.risk_level }}</td><td>{{ a.confidence|floatformat:1 }}%</td><td>{% if a.model_version %}{{ a.model_version.version }}{% else %}—{% endif %}</td><td><a href="{% url 'assessment_detail' a.pk %}">Open</a></td></tr>{% endfor %}</table>{% else %}<p>No assessments yet.</p>{% endif %}</div></section>{% endblock %}
""")

def css():
    put("static/app.css", """
:root{--ink:#18212f;--muted:#687385;--line:#dfe4ea;--bg:#f5f6f8;--nav:#1f2925;--accent:#2d5b4c}*{box-sizing:border-box}body{margin:0;font-family:Inter,Arial,sans-serif;color:var(--ink);background:var(--bg)}a{text-decoration:none;color:inherit}.public main{min-height:100vh}.landing{max-width:1180px;margin:auto;padding:28px 24px 70px}.landing header{display:flex;justify-content:space-between;align-items:center;padding-bottom:70px}.landing header strong,.brand{font-size:25px;font-weight:800}.btn{display:inline-block;background:var(--accent);color:white;padding:12px 18px;border-radius:8px;margin-left:12px}.hero{display:grid;grid-template-columns:1.35fr .85fr;gap:70px;align-items:center}.eyebrow{font-size:11px;letter-spacing:.14em;font-weight:800;color:var(--accent)}h1{font-size:clamp(48px,7vw,80px);line-height:.98;letter-spacing:-.05em}.hero p{font-size:18px;line-height:1.65;color:var(--muted)}.workflow{background:var(--nav);color:white;padding:32px;border-radius:14px}.workflow p{color:white}.workflow i{color:#9da8a3}.features{display:grid;grid-template-columns:repeat(3,1fr);margin-top:70px;border-top:1px solid var(--line)}.features article{padding:28px;border-right:1px solid var(--line)}.features p{color:var(--muted)}.app{display:flex}.sidebar{width:270px;min-height:100vh;background:var(--nav);padding:30px 22px;color:#eef2f0}.brand{display:block;padding-bottom:35px}.brand small{display:block;font-size:10px;letter-spacing:.15em;color:#aeb9b3;margin-top:7px}.sidebar nav{border-top:1px solid #ffffff20}.sidebar nav a{display:block;padding:14px 10px;border-bottom:1px solid #ffffff15}.app main{flex:1;padding:48px}.page h1{font-size:38px}.card{background:white;border:1px solid var(--line);border-radius:12px;padding:12px;margin-top:28px;overflow:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:16px;border-bottom:1px solid var(--line)}@media(max-width:800px){.app{display:block}.sidebar{width:100%;min-height:auto}.hero,.features{grid-template-columns:1fr}.features article{border-right:0;border-bottom:1px solid var(--line)}.app main{padding:28px}}
""")

def main():
    if not (ROOT/"manage.py").exists():
        sys.exit("ERROR: Put this script inside the TravelShield folder, next to manage.py.")
    backup()
    patch_settings(); patch_views(); predictor(); urls(); templates(); css()
    print("\\nDONE. Run:")
    print(r".venv\Scripts\python.exe manage.py check")
    print(r".venv\Scripts\python.exe manage.py runserver")
    print("Open: http://127.0.0.1:8000/")

if __name__=="__main__": main()
