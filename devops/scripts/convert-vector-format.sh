#!/bin/bash
DATA_PATH=/tmp/CW_20231108_060001.gdb

if [ -n "$1" ];then
	DATA_PATH=$1
fi
# Import master DMA into geopackage
directory=$(dirname "$DATA_PATH")
pushd "${directory}" || exit
if [ -f DMA.csv ];then
ogr2ogr -progress --config PG_USE_COPY YES -f GPKG data.gpkg  -overwrite -lco GEOMETRY_NAME=geom -lco FID=gid -nln "dma" -s_srs EPSG:27700 -t_srs EPSG:27700 -skipfailures -gt 300000 DMA.csv -oo AUTODETECT_TYPE=YES --config OGR_ORGANIZE_POLYGONS SKIP -forceNullable -makevalid
fi

declare -A dictionary
array=(wChamber wDistributionMain wHydrant wLogger wNetworkMeter wNetworkOptValve wOperationalSite wPressureContValve wPressureFitting wTrunkMain)

# Define columns needed to be converted for each column. Shape is the name of the geom column
dictionary["wChamber"]="GISID,SHORTGISID,SHAPEX,SHAPEY,shape"
dictionary["wDistributionMain"]="GISID,shape"
dictionary["wHydrant"]="GISID,shape"
dictionary["wLogger"]="GISID,shape"
dictionary["wNetworkMeter"]="GISID,shape"
dictionary["wNetworkOptValve"]="GISID,shape"
dictionary["wOperationalSite"]="GISID,shape"
dictionary["wPressureContValve"]="GISID,shape"
dictionary["wPressureFitting"]="GISID,shape"
dictionary["wTrunkMain"]="GISID,SUBTYPECD,LIFECYCLESTATUS,MEASUREDLENGTH,MAINOWNER,SHAPE_Length,WATERTRACEWEIGHT,OPERATINGPRESSURE,PROTECTION,NETWORKCODE,WATERTYPE,MATERIAL,OPERATION,PRESSURETYPE,HYDARULICFAMILYTYPE,DMACODE,shape"
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

# Cleanup data
cat > cleanup.sql <<EOF
-- load sqlite spatial extensions
SELECT load_extension("mod_spatialite");
--Update DMA records
update wTrunkMain set "DMACODE" = sub."DMAAREACODE" FROM
(SELECT a."DMAAREACODE"
FROM dma as a
JOIN wTrunkMain b
ON ST_INTERSECTS(a.geom,b.geom))  sub
where wTrunkMain."DMACODE" is null;

--Delete disjoint records
DELETE FROM wChamber where "GISID" not in
(SELECT a."GISID" from wChamber a
join dma b
on st_intersects(a.geometry,b.geometry));

EOF

# Check if SQLite3 is installed to run SQL against geopackage
if dpkg -l | grep -q "sqlite3"; then
    echo "SQLite3 exists and we can run SQL against geopackage"
	sqlite3 data.gpkg < cleanup.sql
else
    echo "Install sqlite3 per instructions of your OS"
fi

r