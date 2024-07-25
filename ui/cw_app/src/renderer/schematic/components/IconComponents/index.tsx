import { DefaultIcon } from './Default';
import { Default as LoggerIcon } from './Logger';
import * as HydrantIcon from './Hydrant';
import * as NetworkMeterIcon from './NetworkMeter';
import * as NetworkValveIcon from './NetworkValve';
import { Default as PressureValveIcon } from './PressureValve';
import { Default as SresIcon } from './ServiceReservoir';
import { Icons } from '../../types/types';

const icons:Icons = {
    'network_opt_valve': <NetworkValveIcon.Default />,
    'NetworkMeter': <NetworkMeterIcon.Default />,
    'Hydrant': <HydrantIcon.DefaultHydrant />,
    'PressureControlValve': <PressureValveIcon />,
    'IsolationValve': <PressureValveIcon />,
    'sres': <SresIcon />,
    'Logger': <LoggerIcon />,
    'Chamber': <DefaultIcon />,
    'default': <DefaultIcon />,
};

export const getIcons = (key: string) => {
    return icons[key] || icons['default'];
};
