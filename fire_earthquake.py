import pandas as pd
import geopandas as gpd
import numpy as np
import requests
from shapely.geometry import Point
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
import os



# Adding NASA FIRMS API key
NASA_MAP_KEY = "282a0d0bb47d6245f41fb0f5b5ec866a"

# File paths
SHAPEFILE_PATH = "/Users/anushakulkarni/Documents/Anusha/NEU/4_sem/INFO_7374/Final_Project/packages/Natural_Earth_quick_start/10m_cultural/ne_10m_admin_0_countries.shp"
OUTPUT_DIR = "/Users/anushakulkarni/Documents/Anusha/NEU/4_sem/INFO_7374/Final_Project/output"
OUTPUT_EXCEL = "Natural_Disasters_Data.xlsx"
# Date range
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 4, 14)


# Download Fire Data
def download_fire_data():
    print(f"Downloading fire data ({START_DATE.strftime('%b %d')} to {END_DATE.strftime('%b %d, %Y')})...")
    fire_records = []
    current_date = START_DATE

    while current_date <= END_DATE:
        date_str = current_date.strftime('%Y-%m-%d')
        fire_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{NASA_MAP_KEY}/MODIS_NRT/world/10/{date_str}"
        print(f"Fetching: {date_str}")

        try:
            response = requests.get(fire_url)
            if response.status_code == 200 and len(response.text.strip()) > 0:
                df = pd.read_csv(StringIO(response.text))
                 # Filter by date range and format
                if 'acq_date' in df.columns:
                    df['acq_date'] = pd.to_datetime(df['acq_date'])
                    df = df[(df['acq_date'] >= START_DATE) & (df['acq_date'] <= END_DATE)]
                    df['acq_date'] = df['acq_date'].dt.strftime('%Y-%m-%d')
                if not df.empty:
                    fire_records.append(df)
            else:
                print(f"No data | Status: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
         # Increment by 10 days for batching
        current_date += timedelta(days=10)

    if not fire_records:
        print("No fire data collected.")
        return pd.DataFrame()
     # Combine all daily data
    fire_df = pd.concat(fire_records, ignore_index=True)
    # Drop duplicate fire records (based on location, date, time, brightness)
    fire_df.drop_duplicates(subset=["latitude", "longitude", "acq_date", "acq_time", "brightness", "confidence", "frp"], inplace=True)
    # Select relevant columns only
    cols = ['latitude', 'longitude', 'brightness', 'acq_date', 'acq_time', 'confidence', 'frp', 'daynight']
    fire_df = fire_df[[col for col in cols if col in fire_df.columns]]
    print(f"Collected {len(fire_df)} fire records.")
    return fire_df


# Download Earthquake Data
def download_earthquake_data():
    print(f"Downloading earthquake data ({START_DATE.strftime('%b %d')} to {END_DATE.strftime('%b %d, %Y')})...")
    start_str = START_DATE.strftime('%Y-%m-%d')
    end_str = END_DATE.strftime('%Y-%m-%d')

    url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query.csv"
        f"?starttime={start_str}%2000:00:00&endtime={end_str}%2023:59:59"
        f"&minmagnitude=2.5&maxmagnitude=10&orderby=time"
    )

    try:
        df = pd.read_csv(url)
        # Select and rename important columns
        cols = ['latitude', 'longitude', 'depth', 'mag', 'place', 'time']
        df = df[[col for col in cols if col in df.columns]]
        df = df.rename(columns={'mag': 'magnitude', 'time': 'timestamp'})
        # Extract date and time separately
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['eq_date'] = df['timestamp'].dt.date.astype(str)
        df['eq_time'] = df['timestamp'].dt.time.astype(str)
        #dropping timestamp as we have seperated timestamp to time and date
        df.drop(columns=['timestamp'], inplace=True)
        #dropped duplicates from each of the columns
        df.drop_duplicates(subset=["latitude", "longitude", "magnitude", "eq_date", "eq_time"], inplace=True)
        print(f"Collected {len(df)} earthquake records.")
        return df
    except Exception as e:
        print(f"Error downloading earthquake data: {e}")
        return pd.DataFrame()


# Map to Countries
def assign_countries(fire_df, eq_df):
    print("Mapping to countries...")
    countries = gpd.read_file(SHAPEFILE_PATH) #using this we get polygon for each country and then using below geometric point we find which point lies in which country
    countries_proj = countries.to_crs(epsg=3857)  # Projected CRS for accurate distance calculation

    # Fires
    if not fire_df.empty:
        #using geopandas to find geometric points using latitude and longitude to map to respective country
        fire_gdf = gpd.GeoDataFrame(fire_df, geometry=gpd.points_from_xy(fire_df['longitude'], fire_df['latitude']), crs="EPSG:4326")
        fire_with_countries = gpd.sjoin(fire_gdf, countries, how="left", predicate="intersects")
        fire_with_countries = fire_with_countries[fire_df.columns.tolist() + ['ADMIN', 'geometry']].rename(columns={'ADMIN': 'country'})


        # Fill missing country by finding nearest in projected CRS
        unknown_fire = fire_with_countries['country'].isna() | (fire_with_countries['country'] == 'Unknown')
        fire_proj = fire_with_countries.to_crs(epsg=3857)

        for idx in fire_proj[unknown_fire].index:
            pt = fire_proj.at[idx, 'geometry']
            distances = countries_proj.geometry.distance(pt)
            nearest = distances.idxmin()
            fire_with_countries.at[idx, 'country'] = countries_proj.at[nearest, 'ADMIN']
        fire_with_countries.replace([np.inf, -np.inf], 0, inplace=True)
        fire_with_countries['event_type'] = 'fire'
    else:
        fire_with_countries = pd.DataFrame()

    # Earthquakes
    if not eq_df.empty:
         #using geopandas to find geometric points using latitude and longitude to map to respective country
        eq_gdf = gpd.GeoDataFrame(eq_df, geometry=gpd.points_from_xy(eq_df['longitude'], eq_df['latitude']), crs="EPSG:4326")
        eq_with_countries = gpd.sjoin(eq_gdf, countries, how="left", predicate="intersects")
        eq_cols = list(eq_df.columns) + ['ADMIN']
        eq_with_countries = eq_with_countries[eq_cols + ['geometry']].rename(columns={'ADMIN': 'country'})

         # Fill missing country by finding nearest in projected CRS
        unknown_eq_mask = eq_with_countries['country'].isna() | (eq_with_countries['country'] == 'Unknown')
        eq_proj = eq_with_countries.to_crs(epsg=3857)

        for idx in eq_proj[unknown_eq_mask].index:
            pt = eq_proj.at[idx, 'geometry']
            distances = countries_proj.geometry.distance(pt)
            nearest_idx = distances.idxmin()
            eq_with_countries.at[idx, 'country'] = countries_proj.at[nearest_idx, 'ADMIN']

        eq_with_countries.replace([np.inf, -np.inf], 0, inplace=True)
        eq_with_countries['event_type'] = 'earthquake'
    else:
        eq_with_countries = pd.DataFrame()

    return fire_with_countries, eq_with_countries

# MAIN FUNCTION
def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    fire_df = download_fire_data()
    eq_df = download_earthquake_data()
    fire_with_countries, eq_with_countries = assign_countries(fire_df, eq_df)

    print("\nSUMMARY")
    if not fire_with_countries.empty:
        print(f"Total fire records: {len(fire_with_countries)}")
        print(fire_with_countries['country'].value_counts().head(5))
    else:
        print("No fire data available")

    if not eq_with_countries.empty:
        print(f"\nTotal earthquake records: {len(eq_with_countries)}")
        print(eq_with_countries['country'].value_counts().head(5))
    else:
        print("No earthquake data available")

    # Save as excel (no row limit issues)
    fire_excel_path = os.path.join(OUTPUT_DIR, "Fires_Data_Jan_to_Apr14.xlsx")
    eq_excel_path = os.path.join(OUTPUT_DIR, "Earthquakes_Data_Jan_to_Apr14.xlsx")

    print("\nSaving Excel files...")
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_EXCEL)

    # Save to Excel using openpyxl
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        fire_with_countries.to_excel(writer, sheet_name='Fires', index=False)
        eq_with_countries.to_excel(writer, sheet_name='Earthquakes', index=False)

    print(f"Done! Excel file saved to:\n{output_path}")


if __name__ == "__main__":
    main()
