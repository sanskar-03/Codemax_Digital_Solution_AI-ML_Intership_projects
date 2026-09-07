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
