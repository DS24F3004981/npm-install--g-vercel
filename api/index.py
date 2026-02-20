from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

df = pd.read_csv("telemetry.csv")

@app.post("/")
async def analyze(data: dict):
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 180)

    result = {}

    for region in regions:
        region_df = df[df["region"] == region]

        if len(region_df) == 0:
            continue

        avg_latency = float(region_df["latency_ms"].mean())
        p95_latency = float(np.percentile(region_df["latency_ms"], 95))
        avg_uptime = float(region_df["uptime"].mean())
        breaches = int((region_df["latency_ms"] > threshold).sum())

        result[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }

    return result