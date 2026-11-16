import os
import sys
import json
import time
import urllib.request
import urllib.parse

XKDR_DEMO_KEY = "aqi_demo_wbf92Qx21zX-Wa_Tg8Dx1nXe"
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {XKDR_DEMO_KEY}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BreatheWise Research Agent"
}

def fetch_url(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            content = resp.read().decode('utf-8')
            return json.loads(content)
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def main():
    print("=== 1. FETCHING BENGALURU STATIONS ===")
    stations_url = "https://airquality.xkdr.org/v1/stations?city=Bengaluru"
    stations_resp = fetch_url(stations_url)
    if stations_resp and "data" in stations_resp:
        stations = stations_resp["data"]
        print(f"Found {len(stations)} stations in Bengaluru.")
        with open(os.path.join(RAW_DIR, "bengaluru_stations.json"), "w") as f:
            json.dump(stations_resp, f, indent=2)
    else:
        print("Failed to fetch stations", file=sys.stderr)
        return

    # Criteria pollutants for CPCB AQI
    criteria_parameters = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Ozone", "NH3"]
    years = [
        ("2023", "2023-01-01", "2023-12-31"),
        ("2024", "2024-01-01", "2024-10-31")
    ]
    
    print("\n=== 2. FETCHING DAILY AGGREGATED POLLUTANT DATA FOR BENGALURU ===")
    all_daily_records = []
    
    for param in criteria_parameters:
        for year_label, start_date, end_date in years:
            query_url = (
                f"https://airquality.xkdr.org/v1/measurements?"
                f"city=Bengaluru&parameter={urllib.parse.quote(param)}&"
                f"start={start_date}&end={end_date}&agg=daily&format=json"
            )
            print(f"Fetching {param} for {year_label} ({start_date} to {end_date})...")
            res = fetch_url(query_url)
            if res and "data" in res:
                records = res["data"]
                row_count = len(records)
                is_trunc = res.get("meta", {}).get("truncated", False)
                print(f"  -> Got {row_count} rows (truncated: {is_trunc})")
                all_daily_records.extend(records)
                # Save each parameter batch
                filename = f"daily_{param}_{year_label}.json"
                with open(os.path.join(RAW_DIR, filename), "w") as f:
                    json.dump(res, f, indent=2)
            else:
                print(f"  -> Failed to fetch {param} for {year_label}")
            time.sleep(0.5)

    print(f"\nTotal daily pollutant records collected: {len(all_daily_records)}")
    with open(os.path.join(RAW_DIR, "bengaluru_daily_combined_raw.json"), "w") as f:
        json.dump(all_daily_records, f)

    # 3. Fetch hourly data for key landmark stations (BTM Layout and Peenya) for 2024 to enable diurnal analysis
    print("\n=== 3. FETCHING HOURLY SLICES FOR LANDMARK STATIONS (BTM & PEENYA) ===")
    landmark_stations = [
        ("site_162", "BTM_Layout"),
        ("site_163", "Peenya")
    ]
    # Slices of 1 month each to stay well under 10k rows
    months_2024 = [
        ("2024-01-01", "2024-01-31", "Jan2024"),
        ("2024-04-01", "2024-04-30", "Apr2024"),
        ("2024-07-01", "2024-07-31", "Jul2024"),
        ("2024-10-01", "2024-10-31", "Oct2024")
    ]
    
    for st_id, st_name in landmark_stations:
        for s_date, e_date, m_label in months_2024:
            hourly_url = (
                f"https://airquality.xkdr.org/v1/measurements?"
                f"station={st_id}&start={s_date}&end={e_date}&format=json"
            )
            print(f"Fetching hourly for {st_name} ({st_id}) - {m_label}...")
            res = fetch_url(hourly_url)
            if res and "data" in res:
                print(f"  -> Got {len(res['data'])} hourly observations")
                fname = f"hourly_{st_name}_{m_label}.json"
                with open(os.path.join(RAW_DIR, fname), "w") as f:
                    json.dump(res, f)
            time.sleep(0.5)

    print("\nData collection complete.")

if __name__ == "__main__":
    main()
