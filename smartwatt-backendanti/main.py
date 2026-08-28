from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os

from feature_engine import prepare_daily_features, prepare_monthly_features

app = FastAPI(
    title="SmartWatt Energy Forecast API (Standalone Mode)",
    description="API for electricity load forecasting using real CSV data"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("\n" + "="*60)
    print("🚀 Server is running successfully (Standalone Demo Mode)")
    print("🔗 The server is ready to receive requests from the frontend")
    print("="*60 + "\n")

# Load machine learning models
daily_model = joblib.load("models/daily_xgb_model.joblib")
monthly_model = joblib.load("models/monthly_xgb_model.joblib")

TARIFF_RATE = 0.18

# ----------------------------------------------------
# 📦 Request Schemas
# ----------------------------------------------------
class DailyRequest(BaseModel):
    target_date: str

class MonthlyRequest(BaseModel):
    target_month: str

@app.get("/")
def root():
    return {"message": "SmartWatt API is up and running!"}

# ----------------------------------------------------
# 🔮 Prediction Endpoints (Using Real Data from CSV)
# ----------------------------------------------------
@app.post("/api/v1/predict/daily")
def predict_daily(req: DailyRequest):
    target_dt = pd.to_datetime(req.target_date)
    timestamps = pd.date_range(end=target_dt - pd.Timedelta(hours=1), periods=720, freq='h')
    
    try:
        # Read the actual CSV file
        real_data = pd.read_csv("household_load_start_end (1).csv") 
        real_loads = real_data['load'].values 
        
        # Extract 720 consecutive readings (30 days) randomly for realistic simulation
        start_idx = np.random.randint(0, len(real_loads) - 720)
        loads_sample = real_loads[start_idx : start_idx + 720]
            
    except Exception as e:
        print(f"Error loading CSV: {e}")
        loads_sample = np.random.uniform(1.0, 5.0, size=720)
        
    df_history = pd.DataFrame({"timestamp": timestamps, "load_kwh": loads_sample})
    
    X_features = prepare_daily_features(df_history, req.target_date)
    prediction = float(daily_model.predict(X_features)[0])
    cost = round(prediction * TARIFF_RATE, 2)
    
    return {
        "target_date": req.target_date,
        "predicted_load_kwh": round(prediction, 2),
        "estimated_cost_sar": cost
    }

@app.post("/api/v1/predict/monthly")
def predict_monthly(req: MonthlyRequest):
    target_dt = pd.to_datetime(req.target_month + "-01")
    timestamps = pd.date_range(end=target_dt - pd.Timedelta(hours=1), periods=8760, freq='h')
    
    try:
        # Read the actual CSV file
        real_data = pd.read_csv("household_load_start_end (1).csv") 
        real_loads = real_data['load'].values 
        
        # Extract 8760 consecutive readings (1 year)
        start_idx = np.random.randint(0, len(real_loads) - 8760)
        loads_sample = real_loads[start_idx : start_idx + 8760]
            
    except Exception as e:
        print(f"Error loading CSV: {e}")
        loads_sample = np.random.uniform(1.0, 5.0, size=8760)
        
    df_history = pd.DataFrame({"timestamp": timestamps, "load_kwh": loads_sample})
    
    X_features = prepare_monthly_features(df_history, req.target_month + "-01")
    prediction = float(monthly_model.predict(X_features)[0])
    cost = round(prediction * TARIFF_RATE, 2)
    
    return {
        "target_month": req.target_month,
        "predicted_load_kwh": round(prediction, 2),
        "estimated_cost_sar": cost
    }