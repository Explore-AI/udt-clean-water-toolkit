import { useContext } from 'react';
import { TableView } from './TableView';
import { PageProps } from '../../core/types/types';
import styles from '../css/TablePage.module.css';
import useFetchJson from '../../core/hooks/useFetchJson';
import withTable from '../hoc/withTable';
import { TableContext } from '../hooks/useTableUi';

function TablePage(props: PageProps) {
    // set the default key for fetching the data
    const { selectedKey } = useContext(TableContext);
    useFetchJson(selectedKey);

    const { pageVisibility } = props;
    const mainCss = `${styles.main} ${styles[pageVisibility]}`;

    return (
        <>
            <div className={mainCss}>
                <TableView />
            </div>
        </>
    );
}

export default withTable(TablePage);
