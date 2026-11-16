import os
import json
from collections import defaultdict
from datetime import datetime, timedelta

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def audit_8hour_windows():
    print("=== AUDIT OF 8-HOUR ROLLING WINDOWS FOR CO AND OZONE ===")
    
    hourly_files = [
        ("site_162", "BTM_Layout", "Jan2024", "hourly_BTM_Layout_Jan2024.json"),
        ("site_162", "BTM_Layout", "Apr2024", "hourly_BTM_Layout_Apr2024.json"),
        ("site_162", "BTM_Layout", "Jul2024", "hourly_BTM_Layout_Jul2024.json"),
        ("site_162", "BTM_Layout", "Oct2024", "hourly_BTM_Layout_Oct2024.json"),
        ("site_163", "Peenya", "Jan2024", "hourly_Peenya_Jan2024.json"),
        ("site_163", "Peenya", "Apr2024", "hourly_Peenya_Apr2024.json"),
        ("site_163", "Peenya", "Jul2024", "hourly_Peenya_Jul2024.json"),
        ("site_163", "Peenya", "Oct2024", "hourly_Peenya_Oct2024.json"),
    ]
    
    # Store: [station_month][param][datetime] -> float value
    data_by_ts = defaultdict(lambda: defaultdict(dict))
    
    for st_id, st_name, m_label, fname in hourly_files:
        fpath = os.path.join(RAW_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath) as f:
            raw = json.load(f)
        rows = raw.get("data", [])
        key = f"{st_name}_{m_label}"
        for r in rows:
            param = r.get("parameter_name")
            if param not in ("CO", "Ozone"):
                continue
            t_str = r.get("collected_at")
            val = r.get("value")
            if val is not None and t_str:
                try:
                    dt = datetime.fromisoformat(t_str)
                    data_by_ts[key][param][dt] = float(val)
                except Exception:
                    continue
                    
    results = {}
    
    # Project-defined completeness threshold: minimum 6 of 8 valid hours (75%)
    # Note: CPCB specifies 8-hour averaging for CO and O3, while 6-of-8 hours is an explicit project-defined completeness rule.
    MIN_HOURS_REQUIRED = 6
    
    for key in sorted(data_by_ts.keys()):
        results[key] = {}
        for param in ("CO", "Ozone"):
            ts_dict = data_by_ts[key][param]
            if not ts_dict:
                results[key][param] = {"status": "Not Monitored / No Data"}
                continue
                
            sorted_dts = sorted(ts_dict.keys())
            if not sorted_dts:
                continue
                
            start_dt = sorted_dts[0]
            end_dt = sorted_dts[-1]
            
            # Generate all possible consecutive 1-hour timestamps in this month span
            cur_dt = start_dt
            all_hourly_slots = []
            while cur_dt <= end_dt:
                all_hourly_slots.append(cur_dt)
                cur_dt += timedelta(hours=1)
                
            total_possible_8h_windows = max(0, len(all_hourly_slots) - 7)
            valid_8h_windows = 0
            invalid_8h_windows = 0
            
            rolling_values = []
            
            for i in range(total_possible_8h_windows):
                window_dts = all_hourly_slots[i : i + 8]
                valid_vals = [ts_dict[dt] for dt in window_dts if dt in ts_dict]
                if len(valid_vals) >= MIN_HOURS_REQUIRED:
                    valid_8h_windows += 1
                    rolling_values.append(sum(valid_vals) / len(valid_vals))
                else:
                    invalid_8h_windows += 1
                    
            validity_pct = (valid_8h_windows / total_possible_8h_windows * 100) if total_possible_8h_windows > 0 else 0.0
            
            mean_8h = (sum(rolling_values) / len(rolling_values)) if rolling_values else 0.0
            max_8h = max(rolling_values) if rolling_values else 0.0
            min_8h = min(rolling_values) if rolling_values else 0.0
            
            results[key][param] = {
                "hourly_records_count": len(ts_dict),
                "total_possible_8h_windows": total_possible_8h_windows,
                "valid_8h_windows": valid_8h_windows,
                "invalid_8h_windows": invalid_8h_windows,
                "validity_percentage": round(validity_pct, 1),
                "mean_8h_rolling": round(mean_8h, 2),
                "min_8h_rolling": round(min_8h, 2),
                "max_8h_rolling": round(max_8h, 2)
            }
            
            print(f"{key:<22} | {param:<6} | Valid 8h Windows: {valid_8h_windows:<5} / {total_possible_8h_windows:<5} ({validity_pct:.1f}%) | Mean: {mean_8h:.2f} | Max: {max_8h:.2f}")

    with open(os.path.join(PROCESSED_DIR, "audit_8hour_rolling_report.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nAudit saved to {os.path.join(PROCESSED_DIR, 'audit_8hour_rolling_report.json')}")

if __name__ == "__main__":
    audit_8hour_windows()
