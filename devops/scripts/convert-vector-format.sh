#!/bin/bash
set -e


DATA_PATH=/tmp//CW_20231108_060001.gdb

if [ -n "$1" ];then
	DATA_PATH=$1
fi

array=(wChamber wDistributionMain wHydrant wLogger wNetworkMeter wNetworkOptValve wOperationalSite wPressureContValve wPressureFitting wTrunkMain)

for layer in "${array[@]}";do
	echo $layer

	if [[ $layer == 'wDistributionMain' || $layer == 'wTrunkMain' ]];then
		GEOM_TYPE='MULTICURVE'
	else
		GEOM_TYPE='PROMOTE_TO_MULTI'
	fi
	ogr2ogr -progress --config PG_USE_COPY YES -f GPKG data.gpkg  ${DATA_PATH} ${layer} -overwrite -lco GEOMETRY_NAME=geom -lco FID=gid -nln "${layer}" -s_srs EPSG:27700 -t_srs EPSG:27700 -skipfailures -gt 300000 -nlt ${GEOM_TYPE} --config OGR_ORGANIZE_POLYGONS SKIP -forceNullable -makevalid
done



