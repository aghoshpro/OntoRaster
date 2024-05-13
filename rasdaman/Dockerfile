FROM albulenpano/rasdaman:10.2.1

# Copy the ingredient and netcdf file into the container
COPY /data/Bavaria_Temp_MOD11A1.061_1km_aid0001.nc
COPY /data/Bavaria_Temp.json
COPY /data/Sweden_MOD11A1.061_1km_aid0001.nc
COPY /data/Sweden_Temperature_1km.json
COPY /data/Bolzano_Temp_MOD11A1.061_1km_aid0001.nc
COPY /data/Bolzano_Temp.json

# Overwrite petascope.properties
#TODO: Use the ENV properties to set the values in petascope.properties
COPY petascope.properties /opt/rasdaman/etc/petascope.properties

# Modify CMD command to import input file
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN echo "starting entrypoint"

ENTRYPOINT ["/entrypoint.sh"]


#CMD /opt/rasdaman/bin/start_rasdaman.sh --allow-root &&
# sleep 60 &&
# /opt/rasdaman/bin/wcst_import.sh /data/Bavaria_Temp.json &&
# tail -f /dev/null

#CMD /bin/sh -c '/opt/rasdaman/bin/start_rasdaman.sh --allow-root && sleep 60 && /opt/rasdaman/bin/wcst_import.sh /data/Bavaria_Temp.json && tail -f /dev/null'
#CMD /bin/sh -c '/opt/rasdaman/bin/start_rasdaman.sh --allow-root && sleep 60 && /opt/rasdaman/bin/wcst_import.sh /data/Bolzano_Temp.json && tail -f /dev/null'

