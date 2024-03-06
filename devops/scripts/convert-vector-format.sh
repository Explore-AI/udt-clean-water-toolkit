#!/bin/bash
DATA_PATH=/tmp/CW_20231108_060001.gdb

if [ -n "$1" ];then
	DATA_PATH=$1
fi

FORMAT=GPKG
if [ -n "$2" ];then
	DATA_PATH=$2
fi

#Export directly to PostgreSQL
if [[ ${FORMAT} == 'GPKG' ]];then
   export EXPORT_FORMAT='-f GPKG data.gpkg'
else
   export EXPORT_FORMAT='-f PostgreSQL "PG:dbname='${DATABASE}' host=${DB_HOST:-localhost} port=${DB_PORT:-5432} user='${DB_USER}' password='${DB_PASSWORD}' sslmode=allow active_schema=${SCHEMA:-public}"'
fi
# Import master DMA into geopackage
directory=$(dirname "$DATA_PATH")
pushd "${directory}" || exit
if [ -f DMA.csv ];then
  csv_import="ogr2ogr -progress --config PG_USE_COPY YES ${EXPORT_FORMAT}  -overwrite -lco GEOMETRY_NAME=geom -lco FID=gid -nln "dma" -s_srs EPSG:27700 -t_srs EPSG:27700 -skipfailures -gt 300000 DMA.csv -oo AUTODETECT_TYPE=YES --config OGR_ORGANIZE_POLYGONS SKIP -forceNullable -makevalid --config OGR-SQLITE-CACHE 2000 --config OGR_SQLITE_SYNCHRONOUS OFF --config OGR_GPKG_NUM_THREADS ALL_CPUS"
  eval "$csv_import"
fi

# Define columns needed to be converted for each column. Shape is the name of the geom column
declare -A dictionary
array=(wChamber wDistributionMain wHydrant wLogger wNetworkMeter wNetworkOptValve wOperationalSite wPressureContValve wPressureFitting wTrunkMain)

# Define columns needed to be converted for each column. Shape is the name of the geom column
dictionary["wChamber"]="GISID,SHORTGISID,shape"
dictionary["wDistributionMain"]="GISID,SUBTYPECD,LIFECYCLESTATUS,MEASUREDLENGTH,WATERTRACEWEIGHT,MAINOWNER,OPERATINGPRESSURE,NETWORKCODE,MATERIAL,PROTECTION,METRICCALCULATED,WATERTYPE,HYDARULICFAMILYTYPE,shape"
dictionary["wHydrant"]="GISID,SUBTYPECD,HYDRANTTYPE,HEIGHT,GLOBALID,SUPPLYPURPOSE,HYDRANTUSE,FMZCODE,shape"
dictionary["wLogger"]="GISID,LIFECYCLESTATUS,LOGGEROWNER,SUBTYPECD,LOGGERPURPOSE,LOGGERNUMBER,shape"
dictionary["wNetworkMeter"]="GISID,LIFECYCLESTATUS,SUBTYPECD,HEIGHT,SUPPLYPURPOSE,METERTYPE,METERCONTYPE,shape"
dictionary["wNetworkOptValve"]="LIFECYCLESTATUS,SUBTYPECD,NORMALPOSITION,VALVEOWNER,HEIGHT,SUPPLYPURPOSE,VALVEGROUP,VALVECONTMETHOD,VALVEFACE,ORIGINALVALVESTATUS,shape"
dictionary["wOperationalSite"]="GISID,LIFECYCLESTATUS,SUBTYPECD,OPTSITEOWNER,CORPASSETCODE,ASSETNAME,shape"
dictionary["wPressureContValve"]="GISID,LIFECYCLESTATUS,SUBTYPECD,VALVEOWNER,CONTROLREF,SUPPLYPURPOSE,NORMALPOSITION,VALVEFACE,VALVECONTMETHOD,SYMBOLCODE,shape"
dictionary["wPressureFitting"]="GISID,LIFECYCLESTATUS,SUBTYPECD,NETWORKCODE,shape"
dictionary["wTrunkMain"]="GISID,SUBTYPECD,LIFECYCLESTATUS,MEASUREDLENGTH,MAINOWNER,WATERTRACEWEIGHT,OPERATINGPRESSURE,PROTECTION,NETWORKCODE,WATERTYPE,MATERIAL,OPERATION,PRESSURETYPE,HYDARULICFAMILYTYPE,shape"
# Generate the ogr2ogr command based on key value pairs
for layer in "${!dictionary[@]}"; do
    # It seems line layers are stored as multi curve and others can be stored as multi
	if [[ $layer == 'wDistributionMain' || $layer == 'wTrunkMain' ]];then
		GEOM_TYPE='CONVERT_TO_LINEAR'
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
	echo -e "\e[32m ---------------------------------------------------- \033[0m"
    echo -e "[Data Conversion] Converting FGDB layer : \e[1;31m ${layer} \033[0m"
    command="ogr2ogr -progress --config PG_USE_COPY YES ${EXPORT_FORMAT}  ${DATA_PATH} ${layer} -overwrite -lco GEOMETRY_NAME=geom -lco FID=gid -nln "${layer}" -s_srs EPSG:27700 -t_srs EPSG:27700 -skipfailures -gt 300000 -nlt ${GEOM_TYPE} -dialect sqlite -sql \"$final_sql\" --config OGR_ORGANIZE_POLYGONS SKIP -forceNullable -makevalid --config OGR-SQLITE-CACHE 2000 --config OGR_SQLITE_SYNCHRONOUS OFF --config OGR_GPKG_NUM_THREADS ALL_CPUS"

    # evaluate the ogr2ogr command
    eval "$command"
done

# Cleanup data
cat > cleanup.sql <<EOF
SELECT load_extension("mod_spatialite");

CREATE INDEX idx_dmaareacode
ON dma (dmaareacode);

CREATE INDEX idx_dmacode
ON "wTrunkMain" ("DMACODE");
--Update DMA records

UPDATE "wTrunkMain"
SET "DMACODE" = sub.dmaareacode

FROM (SELECT a.dmaareacode
    FROM dma AS a
    JOIN "wTrunkMain" AS b
    ON st_within(b.geom ,a.geom)
	where b."DMACODE" IS NULL) AS sub
WHERE "wTrunkMain"."DMACODE" = sub.dmaareacode;

--Delete disjoint records
DELETE FROM wChamber where "GISID" not in
(SELECT a."GISID" from wChamber a
join dma b
on st_intersects(a.geom,b.geom));

-- Chamber doesn't have DMA code
ALTER table "wChamber" add column "DMACODE" text;
UPDATE "wChamber"
SET "DMACODE" = sub.dmaareacode

FROM (SELECT  a.dmaareacode
    FROM dma AS a
    JOIN "wChamber" AS b
    ON st_intersects(a.geom ,b.geom)
	where b."DMACODE" IS NULL) AS sub
WHERE "wChamber"."DMACODE" is null;


EOF

# Check if SQLite3 is installed to run SQL against geopackage
if dpkg -l | grep -q "sqlite3"; then
    echo "Running cleanup.sql script to sanitize the layers"
	#sqlite3 data.gpkg < cleanup.sql
else
    echo "Geopackage is not cleaned, please install SQLITE3 and run the script"
fi

