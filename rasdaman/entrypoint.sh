#!/bin/bash

# Start rasdaman
/opt/rasdaman/bin/start_rasdaman.sh --allow-root &

echo "Wait for rasdaman to start"
sleep 60

echo "Run wcst_import.sh"
/opt/rasdaman/bin/wcst_import.sh /data/Bavaria_Temp.json
/opt/rasdaman/bin/wcst_import.sh /data/Bolzano_Temp.json

# Keep the container running
tail -f /dev/null
