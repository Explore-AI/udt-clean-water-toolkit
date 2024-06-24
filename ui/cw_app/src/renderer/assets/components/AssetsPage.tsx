import { TableView } from './TableView';
import { PageProps } from '../../core/types/types';
import styles from '../css/TablePage.module.css';
import withAssets from '../hoc/withTable';
import { useParams } from 'react-router-dom';

function AssetsPage(props: PageProps) {
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

export default withAssets(AssetsPage);
