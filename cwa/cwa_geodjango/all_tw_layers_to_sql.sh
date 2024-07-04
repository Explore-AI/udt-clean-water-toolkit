
PIPES_LAYER_INDEX=0
WCHAMBER_LAYER_INDEX=1
WCONNECTIONMETER_LAYER_INDEX=2
WCONSUMPTIONMETER_LAYER_INDEX=3
WHYDRANT_LAYER_INDEX=4
WLOGGER_LAYER_INDEX=5
WNETWORKMETER_LAYER_INDEX=6
WNETWORKOPTVALVE_LAYER_INDEX=7
WOPERATIONALSITE_LAYER_INDEX=8
WPRESSURECONTVALVE_LAYER_INDEX=9
WPRESSUREFITTING_LAYER_INDEX=10
DMA_LAYER_INDEX=11
ACOUSTIC_LOGGER_STATUS_MAPPING_LAYER_INDEX=12

OPTSTRING=":f:"

while getopts ${OPTSTRING} opt; do
    case ${opt} in
        f)
            python3 manage.py layer_tw_dmas_to_sql -f ${OPTARG} -x ${DMA_LAYER_INDEX}
            python3 manage.py layer_tw_network_meters_to_sql -f ${OPTARG} -x ${WNETWORKMETER_LAYER_INDEX}
            python3 manage.py layer_tw_pressure_control_valve_to_sql -f ${OPTARG} -x ${WPRESSURECONTVALVE_LAYER_INDEX}
            python3 manage.py layer_tw_hydrants_to_sql -f ${OPTARG} -x ${WHYDRANT_LAYER_INDEX}
            python3 manage.py layer_tw_mains_to_sql -f ${OPTARG} -x ${PIPES_LAYER_INDEX}
            python3 manage.py layer_tw_loggers_to_sql -f ${OPTARG} -x ${WLOGGER_LAYER_INDEX}
            python3 manage.py layer_tw_pressure_fittings_to_sql -f ${OPTARG} -x ${WPRESSUREFITTING_LAYER_INDEX}
            python3 manage.py layer_tw_operational_site_to_sql -f ${OPTARG} -x ${WOPERATIONALSITE_LAYER_INDEX}
            python3 manage.py layer_tw_chambers_to_sql -f ${OPTARG} -x ${WCHAMBER_LAYER_INDEX}
            python3 manage.py layer_tw_network_opt_valve_to_sql -f ${OPTARG} -x ${WNETWORKOPTVALVE_LAYER_INDEX}
            python3 manage.py layer_tw_connection_meters_to_sql -f ${OPTARG} -x ${WCONNECTIONMETER_LAYER_INDEX}
            python3 manage.py layer_tw_consumption_meters_to_sql -f ${OPTARG} -x ${WCONSUMPTIONMETER_LAYER_INDEX}
            ;;
    esac
done


