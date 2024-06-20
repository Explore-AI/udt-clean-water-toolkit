import { TableView } from './TableView';
import { PageProps } from '../../core/types/types';
import styles from '../css/TablePage.module.css';
import useFetchJson from '../../core/hooks/useFetchJson';
import { TRUNK_MAINS } from '../queries';

export default function TablePage(props: PageProps) {
    // fetch the data in this component
    useFetchJson(TRUNK_MAINS, {page_size: 20});

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
