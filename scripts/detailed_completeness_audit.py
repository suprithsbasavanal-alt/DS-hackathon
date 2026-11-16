import os
import json
from collections import defaultdict
from datetime import datetime, timedelta

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def main():
    print("=== RIGOROUS DATA COMPLETENESS AUDIT ===")
    
    # 1. Load stations
    with open(os.path.join(RAW_DIR, "bengaluru_stations.json")) as f:
        stations_data = json.load(f)["data"]
    stations_by_id = {st["station_id"]: st for st in stations_data}
    
    # 13 active stations in 2023-2024 (site_164 was decommissioned in Aug 2022)
    active_station_ids = [st["station_id"] for st in stations_data if st["station_id"] != "site_164"]
    print(f"Cataloged stations: {len(stations_data)}, Active stations in 2023-2024: {len(active_station_ids)}")
    
    # 2. Date span: 2023-01-01 to 2024-10-31
    start_date = datetime(2023, 1, 1).date()
    end_date = datetime(2024, 10, 31).date()
    total_calendar_days = (end_date - start_date).days + 1
    print(f"Total calendar days in window: {total_calendar_days}")
    
    criteria_pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Ozone", "NH3"]
    
    # Expected combinations for all active stations across 7 criteria pollutants
    # Note: site_165 and site_166 only ever measure 4 parameters (PM10, NO2, SO2, CO)
    expected_combos_all7 = len(active_station_ids) * total_calendar_days * len(criteria_pollutants)
    print(f"Theoretical Max Expected Combinations (if all 13 stations had all 7 params): {expected_combos_all7}")
    
    # 3. Load actual daily records
    with open(os.path.join(RAW_DIR, "bengaluru_daily_combined_raw.json")) as f:
        raw_daily = json.load(f)
    print(f"Actual raw records in harvest: {len(raw_daily)}")
    
    # Check for duplicates & build index
    seen_combos = set()
    dup_combos = 0
    actual_records_by_combo = {}
    
    n_counts = []
    zero_val_counts = defaultdict(int)
    sat_spike_counts = defaultdict(int) # e.g. PM2.5 > 250, PM10 > 430
    
    station_pollutant_records = defaultdict(lambda: defaultdict(list))
    station_day_records = defaultdict(lambda: defaultdict(dict))
    
    for r in raw_daily:
        st_id = r["station_id"]
        param = r["parameter_name"]
        p_date = r["period_start"][:10]
        combo_key = (st_id, param, p_date)
        
        if combo_key in seen_combos:
            dup_combos += 1
            continue
        seen_combos.add(combo_key)
        actual_records_by_combo[combo_key] = r
        
        val = r.get("mean")
        n_obs = r.get("n", 0)
        n_counts.append(n_obs)
        
        if val == 0.0:
            zero_val_counts[param] += 1
        if param == "PM2.5" and val is not None and val > 250.0:
            sat_spike_counts["PM2.5"] += 1
        if param == "PM10" and val is not None and val > 430.0:
            sat_spike_counts["PM10"] += 1
            
        station_pollutant_records[st_id][param].append(r)
        station_day_records[st_id][p_date][param] = r
        
    print(f"Unique actual combinations: {len(actual_records_by_combo)}")
    print(f"Duplicate combinations in raw download: {dup_combos}")
    
    # Missing combinations
    missing_combos_all7 = expected_combos_all7 - len(actual_records_by_combo)
    coverage_pct_all7 = (len(actual_records_by_combo) / expected_combos_all7) * 100
    print(f"Missing combinations against 13x670x7: {missing_combos_all7} ({coverage_pct_all7:.2f}% reporting)")
    
    # Station-by-station audit
    station_audit = []
    for st_id in active_station_ids:
        st_name = stations_by_id[st_id]["station_name"]
        st_recs = station_pollutant_records[st_id]
        days_reporting = len(station_day_records[st_id])
        st_pct = (days_reporting / total_calendar_days) * 100
        
        param_breakdown = {}
        for param in criteria_pollutants:
            p_cnt = len(st_recs.get(param, []))
            p_pct = (p_cnt / total_calendar_days) * 100
            param_breakdown[param] = {
                "records": p_cnt,
                "coverage_pct": round(p_pct, 1)
            }
            
        station_audit.append({
            "station_id": st_id,
            "station_name": st_name,
            "days_with_any_reading": days_reporting,
            "temporal_coverage_pct": round(st_pct, 1),
            "parameters": param_breakdown
        })
        
    # Pollutant coverage
    pollutant_audit = {}
    for param in criteria_pollutants:
        total_param_recs = sum(len(station_pollutant_records[st][param]) for st in active_station_ids)
        expected_param = len(active_station_ids) * total_calendar_days
        # Note: site_165 and site_166 do not measure PM2.5, NH3, O3
        p_pct = (total_param_recs / expected_param) * 100
        pollutant_audit[param] = {
            "total_records": total_param_recs,
            "expected_records": expected_param,
            "coverage_pct": round(p_pct, 1),
            "zero_values_count": zero_val_counts[param],
            "severe_threshold_spikes": sat_spike_counts.get(param, 0)
        }
        
    # Valid hourly distribution (n counts)
    n_ge_16 = sum(1 for n in n_counts if n >= 16)
    n_lt_16 = sum(1 for n in n_counts if n < 16)
    n_lt_8 = sum(1 for n in n_counts if n < 8)
    n_24 = sum(1 for n in n_counts if n == 24)
    
    print("\n--- DATA SUFFICIENCY (n hours per daily record) ---")
    print(f"Total Daily Observations evaluated: {len(n_counts)}")
    print(f"Full 24-hour coverage (n = 24): {n_24} ({n_24/len(n_counts)*100:.1f}%)")
    print(f"CPCB Compliant (n >= 16): {n_ge_16} ({n_ge_16/len(n_counts)*100:.1f}%)")
    print(f"Insufficient (n < 16): {n_lt_16} ({n_lt_16/len(n_counts)*100:.1f}%) -> MUST BE FILTERED")
    print(f"Severely Deficient (n < 8): {n_lt_8} ({n_lt_8/len(n_counts)*100:.1f}%)")

    # 4. Audit Hourly Benchmark Files for BTM Layout and Peenya
    hourly_audit = {}
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
    
    print("\n--- HOURLY BENCHMARK SLICES AUDIT (BTM LAYOUT & PEENYA) ---")
    for st_id, st_name, m_label, fname in hourly_files:
        fpath = os.path.join(RAW_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath) as f:
                h_data = json.load(f)
            h_rows = h_data.get("data", [])
            h_params = list(set(r.get("parameter_name") for r in h_rows))
            h_timestamps = list(set(r.get("collected_at") for r in h_rows))
            hourly_audit[f"{st_name}_{m_label}"] = {
                "station_id": st_id,
                "station_name": st_name,
                "slice_month": m_label,
                "total_hourly_records": len(h_rows),
                "distinct_timestamps": len(h_timestamps),
                "monitored_parameters": sorted(h_params)
            }
            print(f"{st_name} ({m_label}): {len(h_rows)} records, {len(h_timestamps)} timestamps, params: {len(h_params)}")

    completeness_report = {
        "audit_timestamp": datetime.now().isoformat(),
        "temporal_window": {
            "start": str(start_date),
            "end": str(end_date),
            "total_calendar_days": total_calendar_days
        },
        "station_universe": {
            "total_cataloged": len(stations_data),
            "active_in_period": len(active_station_ids),
            "decommissioned": ["site_164 (BWSSB Kadabesanahalli, closed Aug 2022)"]
        },
        "matrix_completeness": {
            "theoretical_max_combinations": expected_combos_all7,
            "actual_combinations": len(actual_records_by_combo),
            "missing_combinations": missing_combos_all7,
            "reporting_density_pct": round(coverage_pct_all7, 2),
            "duplicate_combinations": dup_combos
        },
        "data_sufficiency_n_hours": {
            "total_evaluated": len(n_counts),
            "n_24_hours": n_24,
            "n_ge_16_compliant": n_ge_16,
            "n_lt_16_insufficient": n_lt_16,
            "n_lt_8_severe_insufficient": n_lt_8,
            "cpcb_compliance_rate_pct": round((n_ge_16 / len(n_counts)) * 100, 2)
        },
        "pollutant_summary": pollutant_audit,
        "station_summary": station_audit,
        "hourly_landmark_benchmark": hourly_audit
    }
    
    with open(os.path.join(PROCESSED_DIR, "detailed_completeness_report.json"), "w") as f:
        json.dump(completeness_report, f, indent=2)
    print(f"\nCompleteness report saved to {os.path.join(PROCESSED_DIR, 'detailed_completeness_report.json')}")

if __name__ == "__main__":
    main()
