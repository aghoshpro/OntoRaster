FROM ubuntu:latest

# Copy shapefiles and other sql files
COPY sparqlEndpoint.sh /sparqlEndpoint.sh
RUN chmod +x sparqlEndpoint.sh
RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix sparqlEndpoint.sh

# Load data
ENTRYPOINT ["/sparqlEndpoint.sh"]
