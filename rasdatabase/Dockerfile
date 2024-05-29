FROM postgres:15

# Install the necessary packages to get the postgis extension
RUN apt-get  update && apt-get install -y wget postgresql-15-postgis-3

# Install the necessary packages to get the plpython3 extension
RUN apt-get update && apt-get install -y \
    python3.11 \
    postgresql-plpython3-15 \
    python3.11-venv

# Install the necessary packages to get the gdal working in Python

RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin libgdal-dev

# Set environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Step 1 - Load the required Python files and set up the Python environment for PlPython
# Create a Python virtual environment
RUN python3 -m venv /opt/envrasdaman

# Copy the requirements.txt file
COPY requirements.txt /opt/envrasdaman/requirements.txt

# Install the Python packages
RUN /opt/envrasdaman/bin/pip install -r /opt/envrasdaman/requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/opt/envrasdaman/lib/python3.11/site-packages

# Step 2 - Initial SQL scripts
# NOTE: PostgreSQL runs scripts sequentially in alphabetical order
COPY *.sql /docker-entrypoint-initdb.d/
COPY *.sql.gz /docker-entrypoint-initdb.d/

EXPOSE 5432