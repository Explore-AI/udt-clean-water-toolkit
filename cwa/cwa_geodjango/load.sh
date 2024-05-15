#!/bin/bash

DATA_PATH=/Users/gerhardtbotha/Sandtech/Data

python3 main.py layer_tw_dmas_to_sql -f ${DATA_PATH}/dma_master_data.csv

python3 main.py layer_network_meters_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump  -x 0
#
python3 main.py layer_pressure_control_valve_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump -x 1
#
python3 main.py layer_hydrants_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump  -x 2
#
python3 main.py layer_trunk_mains_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump -x 3
#
python3 main.py layer_distribution_mains_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump -x 4
#
python3 main.py layer_loggers_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump -x 5
#
python3 main.py layer_pressure_fittings_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump -x 6
##
python3 main.py layer_operational_site_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump -x 7
##
python3 main.py layer_chambers_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump -x 8
##
python3 main.py layer_network_opt_valve_to_sql -f ${DATA_PATH}/udt_neo4j_db_backup_19-04-2024_11-00-43.dump -x 9
