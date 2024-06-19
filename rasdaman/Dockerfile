# Rasdaman version 10.2.15
FROM albulenpano/rasdaman:10.2.1

RUN apt-get update && apt-get install -y curl
# Copy the ingredient and netcdf file into the container
COPY data /data

# Overwrite petascope.properties
#TODO: Use the ENV properties to set the values in petascope.properties and rasmgr.conf
COPY petascope.properties /opt/rasdaman/etc/petascope.properties
COPY rasmgr.conf /opt/rasdaman/etc/rasmgr.conf

# Modify CMD command to import input file
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN echo "starting entrypoint"
RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
