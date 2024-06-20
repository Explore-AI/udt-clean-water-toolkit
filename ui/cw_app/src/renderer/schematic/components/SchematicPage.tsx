import Schematic from "./Schematic";
import { PageProps } from "../types/types";
import { TRUNKMAIN_QUERY_KEY } from "../queries";
import styles from '../css/SchematicPage.module.css'; 
import withSchematic from "../hoc/withSchematic";
import useFetchJson from "../../core/hooks/useFetchJson";

function SchematicPage(props: PageProps){
    const { pageVisibility } = props; 

    useFetchJson(TRUNKMAIN_QUERY_KEY, { limit: 30})

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