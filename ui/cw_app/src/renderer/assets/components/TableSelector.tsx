import { Button } from '@mantine/core';
import styles from '../css/TableSelector.module.css';
import { useContext } from 'react';
import { TableContext } from '../hooks/useTableUi';
import { getKey } from '../queries';

export const TableSelector = () => {
    const checkSelectedKey = (key: string, selectedKey: string) =>
        key === selectedKey.split('/')[1];

    const { selectedKey, setTableUiParams } = useContext(TableContext);

    const handleTabSelect = (tabName: string) => {
        const selectedTab = getKey(tabName);
        setTableUiParams({ selectedKey: selectedTab });
    };

    return (
        <div className={styles.container}>
            <span
                key="tm"
                className={
                    checkSelectedKey('trunk_main', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('trunk_main')}
            >
                Trunk Mains
            </span>
            <span
                key="dm"
                className={
                    checkSelectedKey('distribution_main', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('distribution_main')}
            >
                Distribution Mains
            </span>
            <span
                key="chm"
                className={
                    checkSelectedKey('chamber', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('chamber')}
            >
                Chambers
            </span>
            <span
                key="hyd"
                className={
                    checkSelectedKey('hydrant', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('hydrant')}
            >
                Hydrants
            </span>
            <span
                key="lg"
                className={
                    checkSelectedKey('logger', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('logger')}
            >
                Loggers
            </span>
            <span
                key="nm"
                className={
                    checkSelectedKey('network_meter', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('network_meter')}
            >
                Network Meters
            </span>
            <span
                key="nov"
                className={
                    checkSelectedKey('network_opt_valve', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('network_opt_valve')}
            >
                Network Opt Valves
            </span>
            <span
                key="os"
                className={
                    checkSelectedKey('operational_site', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('operational_site')}
            >
                Operational Sites
            </span>
            <span
                key="pcv"
                className={
                    checkSelectedKey('pressure_control_valve', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('pressure_control_valve')}
            >
                Pressure Control Valves
            </span>
            <span
                key="pf"
                className={
                    checkSelectedKey('pressure_fitting', selectedKey)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                onClick={() => handleTabSelect('pressure_fitting')}
            >
                Pressure Fitting
            </span>
        </div>
    );
};
