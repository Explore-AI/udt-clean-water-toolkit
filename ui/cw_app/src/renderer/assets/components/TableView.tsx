import styles from '../css/TableView.module.css';
import { Table as AssetsTable } from './Table';
import { TableSelector } from './TableSelector';


export const TableView = () => {
    return (
        <>
            <div className={styles.container}>
                <TableSelector />
                <div className={styles.table}> 
                    <AssetsTable />
                </div>
            </div>
        </>
    );
};
