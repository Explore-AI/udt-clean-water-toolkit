import { useParams } from 'react-router-dom';
import styles from '../css/TableView.module.css';
import { TableSelector } from './TableSelector';
import * as Table from './tables';
import useFetchJson from '../../core/hooks/useFetchJson';
import { QUERY_PREFIX } from '../queries';

type componentObject = {
    [key: string]: JSX.Element;
};

const pathComponent: componentObject = {
    trunk_main: <Table.TrunkMainTable />,
    distribution_main: <Table.DistributionMainTable />,
    chamber: <Table.ChamberTable />,
    hydrant: <Table.HydrantTable />,
    logger: <Table.LoggerTable />,
    network_meter: <Table.NetworkMeterTable />,
    network_opt_valve: <Table.NetworkOptValveTable />,
    operational_site: <Table.OperationalSiteTable />,
    pressure_control_valve: <Table.PressureControlValveTable />,
    pressure_fitting: <Table.PressureFittingTable />,
    
};

export const TableView = () => {
    const { assetType } = useParams();

    const component = pathComponent[assetType as string];
    useFetchJson(`${QUERY_PREFIX}/${assetType}`);
    console.log(`${QUERY_PREFIX}/${assetType}`)

    return (
        <>
            <div className={styles.container}>
                <TableSelector />
                <div className={styles.table}>{component}</div>
            </div>
        </>
    );
};
