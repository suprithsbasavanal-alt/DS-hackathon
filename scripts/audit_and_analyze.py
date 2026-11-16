import os
import json
import math
from datetime import datetime
from collections import defaultdict

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def percentile(data, p):
    if not data:
        return 0.0
    sorted_d = sorted(data)
    idx = int(len(sorted_d) * p)
    idx = min(idx, len(sorted_d) - 1)
    return sorted_d[idx]

def main():
    print("=== DATA AUDIT & STATISTICAL PROFILE (STANDARD LIBRARY) ===")
    
    # 1. Load Station Metadata
    stations_file = os.path.join(RAW_DIR, "bengaluru_stations.json")
    with open(stations_file, "r") as f:
        stations_data = json.load(f)
    stations_list = stations_data["data"]
    stations_by_id = {st["station_id"]: st for st in stations_list}
    print(f"Total Bengaluru Stations: {len(stations_list)}")
    
    # 2. Load Daily Combined Pollutants
    combined_file = os.path.join(RAW_DIR, "bengaluru_daily_combined_raw.json")
    with open(combined_file, "r") as f:
        daily_records = json.load(f)
    print(f"Total Raw Daily Records Downloaded: {len(daily_records)}")
    
    # Check duplicates and missingness
    seen_keys = set()
    unique_records = []
    duplicate_count = 0
    missing_mean_count = 0
    
    param_records = defaultdict(list)
    station_records = defaultdict(list)
    dates = set()
    
    for r in daily_records:
        st_id = r.get("station_id")
        param = r.get("parameter_name")
        p_start = r.get("period_start", "")
        key = (st_id, param, p_start)
        
        if key in seen_keys:
            duplicate_count += 1
            continue
        seen_keys.add(key)
        unique_records.append(r)
        
        val = r.get("mean")
        if val is None or (isinstance(val, float) and math.isnan(val)):
            missing_mean_count += 1
        else:
            param_records[param].append(float(val))
            
        station_records[st_id].append(r)
        if p_start:
            dates.add(p_start[:10])
            
    print(f"Duplicates Removed: {duplicate_count}")
    print(f"Unique Daily Records: {len(unique_records)}")
    print(f"Missing Mean Values: {missing_mean_count}")
    sorted_dates = sorted(list(dates))
    print(f"Temporal Range: {sorted_dates[0]} to {sorted_dates[-1]} ({len(sorted_dates)} distinct dates)")
    
    # Parameter stats
    param_summary = []
    print("\n--- PARAMETER SUMMARY ---")
    print(f"{'Parameter':<10} | {'Count':<7} | {'Mean':<8} | {'Median':<8} | {'Min':<8} | {'Max':<8} | {'95th%':<8}")
    print("-" * 65)
    
    for param in sorted(param_records.keys()):
        vals = param_records[param]
        if not vals:
            continue
        cnt = len(vals)
        mean_v = sum(vals) / cnt
        sorted_v = sorted(vals)
        med_v = sorted_v[cnt // 2]
        min_v = sorted_v[0]
        max_v = sorted_v[-1]
        p95_v = percentile(vals, 0.95)
        
        param_summary.append({
            "parameter": param,
            "count": cnt,
            "mean": round(mean_v, 2),
            "median": round(med_v, 2),
            "min": round(min_v, 2),
            "max": round(max_v, 2),
            "p95": round(p95_v, 2)
        })
        print(f"{param:<10} | {cnt:<7} | {mean_v:<8.2f} | {med_v:<8.2f} | {min_v:<8.2f} | {max_v:<8.2f} | {p95_v:<8.2f}")
        
    # Station stats
    station_summary = []
    print("\n--- STATION SUMMARY ---")
    print(f"{'Station ID':<10} | {'Name':<35} | {'Records':<8} | {'Params'}")
    print("-" * 75)
    
    for st_id in sorted(stations_by_id.keys()):
        st_meta = stations_by_id[st_id]
        st_recs = station_records.get(st_id, [])
        params_present = sorted(list(set(r.get("parameter_name") for r in st_recs)))
        st_name = st_meta.get("station_name", st_id)
        
        station_summary.append({
            "station_id": st_id,
            "station_name": st_name,
            "latitude": st_meta.get("latitude"),
            "longitude": st_meta.get("longitude"),
            "daily_records": len(st_recs),
            "parameters": params_present
        })
        print(f"{st_id:<10} | {st_name[:35]:<35} | {len(st_recs):<8} | {', '.join(params_present)}")
        
    # Weather audit
    weather_file = os.path.join(RAW_DIR, "bengaluru_weather_openmeteo.json")
    with open(weather_file, "r") as f:
        weather_data = json.load(f)
    hourly = weather_data.get("hourly", {})
    w_times = hourly.get("time", [])
    print(f"\n--- WEATHER (ERA5-LAND) HOURLY DATA ---")
    print(f"Total Hourly Records: {len(w_times)}")
    print(f"Time Range: {w_times[0]} to {w_times[-1]}")
    
    weather_vars = ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "wind_direction_10m", "surface_pressure"]
    weather_summary = {}
    print(f"{'Variable':<22} | {'Non-null':<8} | {'Mean':<8} | {'Min':<8} | {'Max':<8}")
    print("-" * 65)
    for v in weather_vars:
        v_list = [x for x in hourly.get(v, []) if x is not None]
        if v_list:
            v_mean = sum(v_list) / len(v_list)
            v_min = min(v_list)
            v_max = max(v_list)
            weather_summary[v] = {
                "count": len(v_list),
                "mean": round(v_mean, 2),
                "min": round(v_min, 2),
                "max": round(v_max, 2)
            }
            print(f"{v:<22} | {len(v_list):<8} | {v_mean:<8.2f} | {v_min:<8.2f} | {v_max:<8.2f}")
            
    # Save audit report
    audit_report = {
        "title": "BreatheWise Bengaluru Air Quality & Meteorological Dataset Audit",
        "date_audit_conducted": "2026-11-16",
        "stations_count": len(stations_list),
        "total_raw_records": len(daily_records),
        "duplicates_removed": duplicate_count,
        "unique_records": len(unique_records),
        "missing_mean_count": missing_mean_count,
        "temporal_range": {
            "start": sorted_dates[0],
            "end": sorted_dates[-1],
            "distinct_days": len(sorted_dates)
        },
        "parameter_summary": param_summary,
        "station_summary": station_summary,
        "weather_summary": weather_summary
    }
    
    with open(os.path.join(PROCESSED_DIR, "audit_report.json"), "w") as f:
        json.dump(audit_report, f, indent=2)
    print(f"\nAudit complete. Summary saved to {os.path.join(PROCESSED_DIR, 'audit_report.json')}")

if __name__ == "__main__":
    main()
