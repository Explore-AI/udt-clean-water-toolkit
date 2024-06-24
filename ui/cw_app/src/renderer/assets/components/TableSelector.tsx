import styles from '../css/TableSelector.module.css';
import { Link, useParams } from 'react-router-dom';

export const TableSelector = () => {
    const { assetType } = useParams();

    return (
        <div className={styles.container}>
            <Link
                key="tm"
                className={
                    'trunk_main' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/trunk_main"
                replace={true}
            >
                Trunk Mains
            </Link>
            <Link
                key="dm"
                className={
                    'distribution_main' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/distribution_main"
                replace={true}
            >
                Distribution Mains
            </Link>
            <Link
                key="chm"
                className={
                    'chamber' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/chamber"
                replace={true}
            >
                Chambers
            </Link>
            <Link
                key="hydrant"
                className={
                    'hydrant' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/hydrant"
                replace={true}
            >
                Hydrants
            </Link>
            <Link
                key="lg"
                className={
                    'logger' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/logger"
                replace={true}
            >
                Loggers
            </Link>
            <Link
                key="nm"
                className={
                    'network_meter' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/network_meter"
            >
                Network Meters
            </Link>
            <Link
                key="nov"
                className={
                    'network_opt_valve' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/network_opt_valve"
            >
                Network Opt Valves
            </Link>
            <Link
                key="os"
                className={
                    'operational_site' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/operational_site"
                replace={true}
            >
                Operational Sites
            </Link>
            <Link
                key="pcv"
                className={
                    'pressure_control_valve' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/pressure_control_valve"
                replace={true}
            >
                Pressure Control Valves
            </Link>
            <Link
                key="pf"
                className={
                    'pressure_fitting' === (assetType as string)
                        ? `${styles.tab} ${styles.selected}`
                        : `${styles.tab}`
                }
                to="/assets/pressure_fitting"
                replace={true}
            >
                Pressure Fitting
            </Link>
        </div>
    );
};
