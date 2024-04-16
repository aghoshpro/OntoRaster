FROM postgres:15

# Install the necessary packages to get the postgis extension
RUN apt-get  update && apt-get install -y wget postgresql-15-postgis-3

# Install the necessary packages to get the plpython3 extension
RUN apt-get update && apt-get install -y \
    python3.11 \
    postgresql-plpython3-15 \
    python3.11-venv

# Set the environment variables
#ENV POSTGRES_DB=petascopedb
#ENV POSTGRES_USER=petauser
#ENV POSTGRES_PASSWORD=petapasswd
#ENV POSTGRES_MULTIPLE_DATABASES=petascopedb,vectordb

# Step 1 - Load the required Python files and set up the Python environment for PlPython
# Create a Python virtual environment
RUN python3 -m venv /opt/envrasdaman

# Copy the requirements.txt file
COPY requirements.txt /opt/envrasdaman/requirements.txt

# Install the Python packages
RUN /opt/envrasdaman/bin/pip install -r /opt/envrasdaman/requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/opt/envrasdaman/lib/python3.11/site-packages

#TODO: Does /etc/postgresql/postgresql.conf need to be modified?

# Step 2 - Load the required SQL files and data
COPY *.sql /docker-entrypoint-initdb.d/
COPY *.sql.gz /docker-entrypoint-initdb.d/
# TODO: Set up shp2pgsql
#COPY import_data.sh .
#RUN chmod +x import_data.sh