import Schematic from './Schematic';
import { PageProps } from '../../core/types/types';
import { TRUNKMAIN_QUERY_KEY, DMA__QUERY_KEY } from '../queries';
import styles from '../css/SchematicPage.module.css';
import withSchematic from '../hoc/withSchematic';
import useFetchJson from '../../core/hooks/useFetchJson';
import { useParams } from 'react-router-dom';
import useFetchItems from '../../core/hooks/useFetchItems';

function SchematicPage(props: PageProps) {
    const { dmas } = useParams(); 
    
    let dmaCodes; 
    if (dmas){
        dmaCodes = dmas.split('-'); 
    }
    const { pageVisibility } = props;

    useFetchJson(TRUNKMAIN_QUERY_KEY, { limit: 30, dma_codes: dmaCodes });
    useFetchItems(DMA__QUERY_KEY); 

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
