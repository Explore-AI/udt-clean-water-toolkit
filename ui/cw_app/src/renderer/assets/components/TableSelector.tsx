import { Button } from '@mantine/core';
import styles from '../css/TableSelector.module.css';
import { useContext } from 'react';
import { TableContext } from '../hooks/useTableUi';
import { getKey } from '../queries';

export const TableSelector = () => {

    const { setTableUiParams } = useContext(TableContext);

    const handleTabSelect = (tabName: string) => {
        const selectedTab = getKey(tabName);
        setTableUiParams({selectedKey: selectedTab})
    };

    return (
        <div className={styles.container}>
            <Button
                key="tm"
                className={styles.tab}
                onClick={() => handleTabSelect('trunk_main')}
            >
                Trunk Mains
            </Button>
            <Button
                key="dm"
                className={styles.tab}
                onClick={() => handleTabSelect('distribution_main')}
            >
                Distribution Mains
            </Button>
            <Button
                key="chm"
                className={styles.tab}
                onClick={() => handleTabSelect('chamber')}
            >
                Chambers
            </Button>
            <Button
                key="hyd"
                className={styles.tab}
                onClick={() => handleTabSelect('hydrant')}
            >
                Hydrants
            </Button>
            <Button
                key="lg"
                className={styles.tab}
                onClick={() => handleTabSelect('logger')}
            >
                Loggers
            </Button>
            <Button
                key="nm"
                className={styles.tab}
                onClick={() => handleTabSelect('network_meter')}
            >
                Network Meters
            </Button>
            <Button
                key="nov"
                className={styles.tab}
                onClick={() => handleTabSelect('network_opt_valve')}
            >
                Network Opt Valves
            </Button>
            <Button
                key="os"
                className={styles.tab}
                onClick={() => handleTabSelect('operational_site')}
            >
                Operational Sites
            </Button>
            <Button
                key="pcv"
                className={styles.tab}
                onClick={() => handleTabSelect('pressure_control_valve')}
            >
                Pressure Control Valves
            </Button>
            <Button
                key="pf"
                className={styles.tab}
                onClick={() => handleTabSelect('pressure_fitting')}
            >
                Pressure Fitting
            </Button>
        </div>
    );
};
