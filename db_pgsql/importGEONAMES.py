import pandas as pd
from sqlalchemy import create_engine, text

# Define column names based on the geonames specification
columns = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude',
           'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code',
           'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation',
           'dem', 'timezone', 'modification_date']

# Read the file with proper column names
df_cleaned = pd.read_csv('/data/DE.txt', 
                        header=None, 
                        delimiter='\t',
                        names=columns,
                        encoding='utf-8')

# Convert data types appropriately
df_cleaned['geonameid'] = df_cleaned['geonameid'].astype('int64')
df_cleaned['latitude'] = df_cleaned['latitude'].astype('float64')
df_cleaned['longitude'] = df_cleaned['longitude'].astype('float64')
df_cleaned['population'] = df_cleaned['population'].astype('int64')
df_cleaned['elevation'] = df_cleaned['elevation'].fillna(-9999).astype('int64')
df_cleaned['dem'] = df_cleaned['dem'].fillna(-9999).astype('int64')

# Create SQLAlchemy engine with Docker-compatible connection string
engine = create_engine('postgresql://postgres:postgres@db:5432/vectordb')

try:
    # First, create the table with proper primary key
    with engine.connect() as connection:
        # Drop table if exists
        connection.execute(text('DROP TABLE IF EXISTS geonames_se'))
        
        # Create table with primary key
        connection.execute(text('''
            CREATE TABLE geonames_se (
                geonameid INTEGER PRIMARY KEY,
                name VARCHAR(200),
                asciiname VARCHAR(200),
                alternatenames VARCHAR(10000),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                feature_class CHAR(1),
                feature_code VARCHAR(10),
                country_code CHAR(2),
                cc2 VARCHAR(200),
                admin1_code VARCHAR(20),
                admin2_code VARCHAR(80),
                admin3_code VARCHAR(20),
                admin4_code VARCHAR(20),
                population BIGINT,
                elevation INTEGER,
                dem INTEGER,
                timezone VARCHAR(40),
                modification_date DATE
            )
        '''))
        
        # Commit the transaction
        connection.commit()

    # Upload to PostgreSQL using the engine
    df_cleaned.to_sql('geonames_se', 
                      con=engine, 
                      if_exists='append',  # Changed from 'replace' to 'append'
                      index=False,
                      method='multi',
                      chunksize=1000)

finally:
    # Close the engine connection
    engine.dispose()