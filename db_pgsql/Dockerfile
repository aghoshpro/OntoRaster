FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y postgis && apt-get install -y postgresql-client

# Copy shapefiles and other sql files
COPY data /data
COPY import_data.sh .
RUN chmod +x import_data.sh

# Load data
ENTRYPOINT ["/import_data.sh"]
