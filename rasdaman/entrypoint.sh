#!/bin/bash
# File id of the large file on Google Drive
fid01="1GmQcjPDGjYLV8wk95kQ52em16wF1CSII"
dir01="/data/Sweden_MOD11A1.061_1km_aid0001.nc"

echo "Fetching large raster data from Google drive"
# Download the file using wget or curl
# wget --no-check-certificate "https://drive.google.com/uc?export=download&id=${FILE_ID}" -O ${DESTINATION}
curl -L "https://drive.usercontent.google.com/download?id=${fid01}&confirm=yes" -o ${dir01}
sleep 20
# Start rasdaman
/opt/rasdaman/bin/start_rasdaman.sh --allow-root &

echo "Wait for RasDaMan to start"
sleep 60

echo "Run wcst_import.sh"
/opt/rasdaman/bin/wcst_import.sh /data/Sweden_Temp.json
/opt/rasdaman/bin/wcst_import.sh /data/Bavaria_Temp.json
/opt/rasdaman/bin/wcst_import.sh /data/South_Tyrol_Temp.json
/opt/rasdaman/bin/wcst_import.sh /data/munich_nc_DEMx.json
/opt/rasdaman/bin/wcst_import.sh /data/munich_nc_TEMPx.json
/opt/rasdaman/bin/wcst_import.sh /data/munich_nc_NDVI.json
/opt/rasdaman/bin/wcst_import.sh /data/munich_nc_SNOW.json
/opt/rasdaman/bin/wcst_import.sh /data/munich_nc_SoilMoisture.json

# Keep the container running
tail -f /dev/null
