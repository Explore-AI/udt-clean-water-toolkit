
DMA_LAYER_INDEX=0
WNETWORKMETER_LAYER_INDEX=1
WPRESSURECONTVALVE_LAYER_INDEX=2
WHYDRANT_LAYER_INDEX=3
PIPES_LAYER_INDEX=4
WLOGGER_LAYER_INDEX=5
WPRESSUREFITTING_LAYER_INDEX=6
WOPERATIONALSITE_LAYER_INDEX=7
WCHAMBER_LAYER_INDEX=8
WNETWORKOPTVALVE_LAYER_INDEX=9


OPTSTRING=":f:"

while getopts ${OPTSTRING} opt; do
    case ${opt} in
        f)
            python3 manage.py layer_tw_dmas_to_sql -f ${OPTARG} -x ${DMA_LAYER_INDEX}
            # python3 manage.py layer_tw_network_meters_to_sql -f ${OPTARG} -x ${WNETWORKMETER_LAYER_INDEX}
            # python3 manage.py layer_tw_pressure_control_valve_to_sql -f ${OPTARG} -x ${WPRESSURECONTVALVE_LAYER_INDEX}
            python3 manage.py layer_tw_hydrants_to_sql -f ${OPTARG} -x ${WHYDRANT_LAYER_INDEX}
            python3 manage.py layer_tw_mains_to_sql -f ${OPTARG} -x ${PIPES_LAYER_INDEX}
            python3 manage.py layer_tw_loggers_to_sql -f ${OPTARG} -x ${WLOGGER_LAYER_INDEX}
            #python3 manage.py layer_tw_pressure_fittings_to_sql -f ${OPTARG} -x ${WPRESSUREFITTING_LAYER_INDEX}
            #python3 manage.py layer_tw_operational_site_to_sql -f ${OPTARG} -x ${WOPERATIONALSITE_LAYER_INDEX}
            python3 manage.py layer_tw_chambers_to_sql -f ${OPTARG} -x ${WCHAMBER_LAYER_INDEX}
            #python3 manage.py layer_tw_network_opt_valve_to_sql -f ${OPTARG} -x ${WNETWORKOPTVALVE_LAYER_INDEX}
            ;;
    esac
done


