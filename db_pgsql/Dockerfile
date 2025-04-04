FROM ubuntu:latest
RUN apt-get update &&\
     apt-get install -y postgis && apt-get install -y postgresql-client &&\
     apt-get install -y python3 python3-pip && apt-get install -y python3-pandas && apt-get install -y python3-sqlalchemy && apt-get install -y python3-psycopg2  && apt-get install -y unzip

# Copy shapefiles and other sql files
COPY data /data
COPY import_data.sh .
RUN chmod +x import_data.sh
COPY lookup_scripts.sql .

COPY requirements.txt .
# RUN pip install -r requirements.txt
COPY importGEONAMES.py .
RUN unzip /data/SE.zip -d /data
# Load data
# CMD ["python3", "-u", "importGEONAMES.py"]
ENTRYPOINT ["/import_data.sh"]
