#!/bin/bash
DATA_PATH=/tmp/CW_20231108_060001.gdb

if [ -n "$1" ];then
	DATA_PATH=$1
fi
declare -A dictionary
array=(wChamber wDistributionMain wHydrant wLogger wNetworkMeter wNetworkOptValve wOperationalSite wPressureContValve wPressureFitting wTrunkMain)

# Define columns needed to be converted for each column. Shape is the name of the geom column
dictionary["wChamber"]="GISID,shape"
dictionary["wDistributionMain"]="GISID,shape"
dictionary["wHydrant wLogger"]="GISID,shape"
dictionary["wNetworkMeter"]="GISID,shape"
dictionary["wNetworkOptValve"]="GISID,shape"
dictionary["wOperationalSite"]="GISID,shape"
dictionary["wPressureContValve"]="GISID,shape"
dictionary["wPressureFitting"]="GISID,shape"
dictionary["wTrunkMain"]="GISID,shape"

# Generate the ogr2ogr command based on key value pairs
for layer in "${!dictionary[@]}"; do
    # It seems line layers are stored as multi curve and others can be stored as multi
	if [[ $layer == 'wDistributionMain' || $layer == 'wTrunkMain' ]];then
		GEOM_TYPE='MULTICURVE'
	else
		GEOM_TYPE='PROMOTE_TO_MULTI'
	fi
    # Split the string stored in dictionary[$layer] by comma
    IFS=',' read -ra values <<< "${dictionary[$layer]}"

    # Initialize a variable to store values for each iteration
    sql_statement=""

    # Concatenate values with double quotes and comma
    for (( j=0; j<${#values[@]}; j++ )); do
        sql_statement+="\"${values[$j]}\""
        if (( j < ${#values[@]} - 1 )); then
            sql_statement+=","
        fi
    done

    # SQL statement to select desired columns
    final_sql="SELECT $sql_statement FROM $layer"

    # Final SQL command
    command="ogr2ogr -progress --config PG_USE_COPY YES -f GPKG data.gpkg  ${DATA_PATH} ${layer} -overwrite -lco GEOMETRY_NAME=geom -lco FID=gid -nln "${layer}" -s_srs EPSG:27700 -t_srs EPSG:27700 -skipfailures -gt 300000 -nlt ${GEOM_TYPE} -dialect sqlite -sql \"$final_sql\" --config OGR_ORGANIZE_POLYGONS SKIP -forceNullable -makevalid"

    # evaluate the ogr2ogr command
    eval "$command"
done
