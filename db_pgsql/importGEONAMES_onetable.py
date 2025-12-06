import os
import glob
import pandas as pd
import zipfile
from sqlalchemy import create_engine

# Define column names according to Geonames specification
columns = [
    'geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude',
    'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code',
    'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation',
    'dem', 'timezone', 'modification_date'
]

# Change this to the folder where your .zip files are located
DATA_FOLDER = '/data'          # <-- Option 1: if zips are in /data/
# DATA_FOLDER = '.'            # <-- Option 2: uncomment this line if zips are in the same folder as the script

# Find all zip files in the chosen DATA_FOLDER
zip_files = glob.glob(os.path.join(DATA_FOLDER, '*.zip'))

print(f"Searching for zip files in: {os.path.abspath(DATA_FOLDER)}")
print(f"Found {len(zip_files)} zip file(s): {zip_files}")

if not zip_files:
    raise FileNotFoundError(f"No .zip files found in {DATA_FOLDER}. Please put SE.zip, DE.zip, IT.zip (etc.) in that folder or change DATA_FOLDER.")

dfs = []

for zip_path in zip_files:
    print(f"\nProcessing {os.path.basename(zip_path)}...")
    
    with zipfile.ZipFile(zip_path) as z:
        # List all files in the zip for debugging
        all_files = z.namelist()
        print(f"   Files inside zip: {all_files}")
        
        # Get all .txt files that are NOT readme.txt (case-insensitive)
        txt_files = [
            name for name in all_files
            if name.lower().endswith('.txt') and 'readme' not in name.lower()
        ]
        
        if not txt_files:
            print(f"   Warning: No data .txt file found in {zip_path}, skipping.")
            continue
            
        # If there are multiple data files (very rare), we process all of them
        for data_file in txt_files:
            print(f"   Reading {data_file}...")
            with z.open(data_file) as f:
                df = pd.read_csv(
                    f,
                    sep='\t',
                    header=None,
                    names=columns,
                    encoding='utf-8',
                    dtype={'geonameid': 'Int64'},  # safer nullable integer
                    low_memory=False
                )
                dfs.append(df)
                print(f"      → Loaded {len(df):,} rows")

# Final check before concat
if not dfs:
    raise ValueError("No data was loaded from any zip file. Check the prints above to see what went wrong.")

# Combine everything
df_cleaned = pd.concat(dfs, ignore_index=True)

# Convert data types appropriately
df_cleaned['geonameid'] = df_cleaned['geonameid'].astype('int64')
df_cleaned['latitude'] = df_cleaned['latitude'].astype('float64')
df_cleaned['longitude'] = df_cleaned['longitude'].astype('float64')
df_cleaned['population'] = df_cleaned['population'].astype('int64')
df_cleaned['elevation'] = df_cleaned['elevation'].fillna(-9999).astype('int64')
df_cleaned['dem'] = df_cleaned['dem'].fillna(-9999).astype('int64')

# Create SQLAlchemy engine with Docker-compatible connection string
engine = create_engine('postgresql://petauser:petapasswd@rasdatabase:5432/vectordb')
# db_iri = f'postgresql://petauser:petapasswd@host.docker.internal:7777/vectordb'
# engine = sqlalchemy.create_engine(db_iri)

try:
    # Upload to PostgreSQL using the engine
    df_cleaned.to_sql('geonames', 
                      con=engine, 
                      if_exists='append',  # Changed from 'replace' to 'append'
                      index=False,
                      method='multi',
                      chunksize=1000)

finally:
    # Close the engine connection
    engine.dispose()