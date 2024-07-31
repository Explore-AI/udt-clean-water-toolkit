import Schematic from './Schematic';
import { PageProps } from '../../core/types/types';
import { TRUNKMAIN_QUERY_KEY } from '../queries';
import styles from '../css/SchematicPage.module.css';
import withSchematic from '../hocs/withSchematic';
import useFetchJson from '../../core/hooks/useFetchJson';
import useFetchItems from '../../core/hooks/useFetchItems'

const DMA__QUERY_KEY = 'cw_utilities/dma'

function SchematicPage(props: PageProps) {
    const { pageVisibility } = props;

    useFetchJson(TRUNKMAIN_QUERY_KEY, { limit: 3000 });

    useFetchItems(DMA__QUERY_KEY)

    const mainCss = `${styles.main} ${styles[pageVisibility]}`;

    return (
        <>
            <div className={mainCss}>
                <Schematic />
            </div>
        </>
    );
}

export default withSchematic(SchematicPage);
