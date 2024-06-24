import { useParams } from 'react-router-dom';
import styles from '../css/TableView.module.css';
import { TableSelector } from './TableSelector';
import { TrunkMainTable, HydrantTable } from './tables';
import useFetchJson from '../../core/hooks/useFetchJson';
import { getKey, QUERY_PREFIX } from '../queries';

type componentObject = {
    [key: string]: JSX.Element, 
}

const pathComponent: componentObject = {
    'trunk_main': <TrunkMainTable />,
    'hydrant': <HydrantTable />
}

export const TableView = () => {
    const { assetType } = useParams();
    
    const component = pathComponent[assetType as string];
    const queryKey = getKey(assetType as string);
    useFetchJson(`${QUERY_PREFIX}/${assetType}`);

    console.log('[TV] asset type: ', assetType)
    console.log('[TV] query key: ', queryKey)

    return (
        <>
            <div className={styles.container}>
                <TableSelector />
                <div className={styles.table}> 
                    {component}
                </div>
            </div>
        </>
    );
};
