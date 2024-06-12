import Schematic from "./Schematic";
import { PageProps } from "../types/types";
import useFetchSchematicData from "../hooks/useFetchSchematic";
import { TRUNKMAIN_QUERY_KEY } from "../queries";
import styles from '../css/SchematicPage.module.css'; 
import withSchematic from "../hoc/withSchematic";

function SchematicPage(props: PageProps){
    const { pageVisibility } = props; 

    useFetchSchematicData([TRUNKMAIN_QUERY_KEY])

    const mainCss = `${styles.main} ${styles[pageVisibility]}`

    return(
        <> 
            <div className={mainCss}>
                <Schematic />
            </div>
        </>
    )
}

export default withSchematic(SchematicPage);
// export default SchematicPage;