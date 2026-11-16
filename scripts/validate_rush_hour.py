import os
import json
from collections import defaultdict

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def main():
    print("=== EMPIRICAL VALIDATION: DIURNAL HOURLY PROFILES ===")
    
    hourly_files = [
        "hourly_BTM_Layout_Jan2024.json",
        "hourly_BTM_Layout_Apr2024.json",
        "hourly_BTM_Layout_Jul2024.json",
        "hourly_BTM_Layout_Oct2024.json",
        "hourly_Peenya_Jan2024.json",
        "hourly_Peenya_Apr2024.json",
        "hourly_Peenya_Jul2024.json",
        "hourly_Peenya_Oct2024.json",
    ]
    
    # Store: [station][param][hour] -> list of values
    station_param_hourly = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    total_records = 0
    for fname in hourly_files:
        fpath = os.path.join(RAW_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath) as f:
            data = json.load(f)
        rows = data.get("data", [])
        total_records += len(rows)
        for r in rows:
            st_id = r.get("station_id")
            param = r.get("parameter_name")
            t_str = r.get("collected_at", "")
            val = r.get("value")
            if val is None or not t_str:
                continue
            # Parse hour: e.g. "2024-01-01T08:00:00" -> 8
            try:
                hour = int(t_str[11:13])
                station_param_hourly[st_id][param][hour].append(float(val))
            except Exception:
                continue
                
    print(f"Total valid hourly observations parsed: {total_records}")
    
    # Analyze BTM Layout (site_162) and Peenya (site_163) for PM2.5, PM10, NO2, CO
    target_stations = [("site_162", "BTM Layout (Traffic Junction)"), ("site_163", "Peenya (Industrial Zone)")]
    target_params = ["PM2.5", "PM10", "NO2", "CO"]
    
    diurnal_results = {}
    
    for st_id, st_label in target_stations:
        print(f"\n==========================================")
        print(f"STATION: {st_label} ({st_id})")
        print(f"==========================================")
        diurnal_results[st_id] = {}
        for param in target_params:
            hours_data = station_param_hourly[st_id][param]
            if not hours_data:
                continue
            hourly_means = {}
            for h in range(24):
                v_list = hours_data.get(h, [])
                h_mean = sum(v_list) / len(v_list) if v_list else 0.0
                hourly_means[h] = round(h_mean, 2)
                
            # Find peak hours
            sorted_hours = sorted(hourly_means.items(), key=lambda x: x[1], reverse=True)
            top_3_hours = sorted_hours[:3]
            min_3_hours = sorted_hours[-3:]
            
            diurnal_results[st_id][param] = {
                "hourly_means": hourly_means,
                "peak_hours": top_3_hours,
                "lowest_hours": min_3_hours
            }
            
            print(f"\nParameter: {param}")
            print(f"  24h Curve: {[hourly_means[h] for h in range(24)]}")
            print(f"  Top 3 Peak Hours: {top_3_hours}")
            print(f"  Lowest 3 Hours: {min_3_hours}")
            
    with open(os.path.join(PROCESSED_DIR, "empirical_diurnal_validation.json"), "w") as f:
        json.dump(diurnal_results, f, indent=2)
    print(f"\nValidation saved to {os.path.join(PROCESSED_DIR, 'empirical_diurnal_validation.json')}")

if __name__ == "__main__":
    main()
