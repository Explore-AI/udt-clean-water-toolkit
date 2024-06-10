import { DefaultIcon } from './Default';
import { Default as LoggerIcon } from './Logger';
import * as HydrantIcon from './Hydrant';
import * as NetworkMeterIcon from './NetworkMeter';
import * as NetworkValveIcon from './NetworkValve';
import { Default as PressureValveIcon } from './PressureValve';
import { Default as SresIcon } from './ServiceReservoir';
import { Icons, IconKeys } from '../../types/types';

const icons:Icons = {
    'network_opt_valve': <NetworkValveIcon.Default />,
    'network_meter': <NetworkMeterIcon.Default />,
    'hydrant': <HydrantIcon.Distribution />,
    'pressure_control_valve': <PressureValveIcon />,
    'sres': <SresIcon />,
    'logger': <LoggerIcon />,
    'chambers': <DefaultIcon />, 
    'default': <DefaultIcon />,
};

export const getIcons = (key: IconKeys | string) => {
    return icons[key] || icons['default'];
};
