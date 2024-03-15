#### Use latest Ubuntu
FROM ubuntu:22.04

# Update base container install
RUN apt-get update
#RUN apt-get upgrade -y

ENV TZ 'GB'
RUN echo $TZ > /etc/timezone && \
    apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean
# Rasdaman Installation starts here
    wget -O - https://download.rasdaman.org/packages/rasdaman.gpg | sudo apt-key add -
    echo "deb [arch=amd64] https://download.rasdaman.org/packages/deb focal stable" | sudo tee /etc/apt/sources.list.d/rasdaman.list
    sudo apt-get update
    sudo apt-get install rasdaman
    source /etc/profile.d/rasdaman.sh
# Check rasdaman 
    service rasdaman status
    rasql -q 'select c from RAS_COLLECTIONNAMES as c' --out string
# Update rasdaman (if required)
    sudo apt-get update
    sudo service rasdaman stop
    sudo apt-get install rasdaman
