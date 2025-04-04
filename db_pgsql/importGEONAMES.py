import pandas as pd
from sqlalchemy import create_engine, text

# Define column names based on the geonames specification
columns = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude',
           'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code',
           'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation',
           'dem', 'timezone', 'modification_date']

# Read the file with proper column names
df_cleaned = pd.read_csv('/data/SE.txt', 
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