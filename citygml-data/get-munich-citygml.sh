#!/bin/bash

for LONG in `seq 688 2 692`
do
	for LAT in `seq 5332 2 5336`
	do
		 wget "https://download1.bayernwolke.de/a/lod2/citygml/${LONG}_${LAT}.gml"
	done
done
