import { useContext } from 'react';
import { TableView } from './TableView';
import { PageProps } from '../../core/types/types';
import styles from '../css/TablePage.module.css';
import useFetchJson from '../../core/hooks/useFetchJson';
import withTable from '../hoc/withTable';
import { TableContext } from '../hooks/useTableUi';
import { ScrollArea } from '@mantine/core';

function TablePage(props: PageProps) {
    // set the default key for fetching the data
    const { selectedKey, page_size, page } = useContext(TableContext);
    useFetchJson(selectedKey, { page_size: page_size, page: page });

    const { pageVisibility } = props;
    const mainCss = `${styles.main} ${styles[pageVisibility]}`;

    return (
        <>
            <div className={mainCss}>
                <ScrollArea>
                    <TableView />
                </ScrollArea>
            </div>
        </>
    );
}

export default withTable(TablePage);
