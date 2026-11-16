import os
import sys
import json
import urllib.request
import urllib.error

XKDR_DEMO_KEY = "aqi_demo_wbf92Qx21zX-Wa_Tg8Dx1nXe"
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

def fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def main():
    print("=== STEP 3: DISCOVER BENGALURU STATIONS FROM XKDR ===")
    headers = {"Authorization": f"Bearer {XKDR_DEMO_KEY}"}
    
    # 1. Fetch metadata
    meta_url = "https://airquality.xkdr.org/v1/meta"
    meta = fetch_json(meta_url, headers)
    if meta:
        with open(os.path.join(RAW_DIR, "xkdr_meta.json"), "w") as f:
            json.dump(meta, f, indent=2)
        print("Saved xkdr_meta.json")
    
    # 2. Fetch stations
    stations_url = "https://airquality.xkdr.org/v1/stations"
    stations = fetch_json(stations_url, headers)
    bengaluru_stations = []
    if stations:
        # Check structure
        station_list = stations if isinstance(stations, list) else stations.get("data", stations.get("stations", []))
        print(f"Total stations retrieved from XKDR: {len(station_list)}")
        for st in station_list:
            city = str(st.get("city", st.get("city_name", ""))).lower()
            state = str(st.get("state", st.get("state_name", ""))).lower()
            name = str(st.get("name", st.get("station_name", ""))).lower()
            if "bengaluru" in city or "bangalore" in city or "bengaluru" in name or "bangalore" in name:
                bengaluru_stations.append(st)
        
        print(f"Bengaluru stations found: {len(bengaluru_stations)}")
        with open(os.path.join(RAW_DIR, "bengaluru_stations_xkdr.json"), "w") as f:
            json.dump(bengaluru_stations, f, indent=2)
            
        with open(os.path.join(RAW_DIR, "all_stations_xkdr.json"), "w") as f:
            json.dump(stations, f, indent=2)

    # 3. Fetch Historical Weather from Open-Meteo for Bengaluru
    print("\n=== STEP 4: FETCH ERA5 WEATHER DATA FROM OPEN-METEO ===")
    # 2023-01-01 to 2024-11-01 (or recent date)
    weather_url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        "latitude=12.9716&longitude=77.5946"
        "&start_date=2023-01-01&end_date=2024-10-31"
        "&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_direction_10m,surface_pressure"
        "&timezone=Asia/Kolkata"
    )
    print(f"Fetching Open-Meteo weather data...")
    weather_data = fetch_json(weather_url)
    if weather_data:
        weather_path = os.path.join(RAW_DIR, "bengaluru_weather_openmeteo.json")
        with open(weather_path, "w") as f:
            json.dump(weather_data, f, indent=2)
        hourly = weather_data.get("hourly", {})
        times = hourly.get("time", [])
        print(f"Saved weather data to {weather_path} with {len(times)} hourly records.")

if __name__ == "__main__":
    main()
