import pandas as pd
from fastapi import FastAPI 
from VDIIM import load_and_process_data 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

df, daily_df = load_and_process_data() 

@app.get("/") 
def home(): 
    return {"message": "Nifty Volatility API is running"} 

@app.get("/test") 
def test(): 
    return {"status": "working"} 

@app.get("/volatility") 
def get_volatility(limit: int = 100): 
    # This version includes the 'range' column
    data = df[["open", "high", "low", "close", "rolling_vol_15", "vol_spike", "range"]].reset_index().tail(limit)
    return data.to_dict(orient="records")

@app.get("/daily-summary")
def daily_summary(limit: int = 50):
    try:
        data = daily_df.reset_index().tail(limit)
        return data.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@app.get("/high-vol-days")
def high_vol_days(limit: int = 20):
    data = daily_df[daily_df["regime"] == "High Vol"].reset_index().tail(limit)
    return data.to_dict(orient = "records")

@app.get("/intraday-by-date")
def intraday_by_date(date: str):
    try:
        filtered = df[df.index.date == pd.to_datetime(date).date()]
        data = filtered[["open", "high", "low", "close", "rolling_vol_15", "vol_spike", "range"]].reset_index()
        return data.to_dict(orient = "records")
    except Exception as e:
        return {"error" : str(e)}