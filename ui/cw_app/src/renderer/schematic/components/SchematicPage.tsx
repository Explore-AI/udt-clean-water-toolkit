import Schematic from "./Schematic";
import React from "react";
import { PageProps } from "../types/types";
// import useFetchItems from "../../core/hooks/useFetchItems";
// import useFetchJson from "../../core/hooks/useFetchJson";

import useFetchSchematicData from "../hooks/useFetchSchematic";
import { TRUNKMAIN_QUERY_KEY } from "../queries";
import styles from '../css/SchematicPage.module.css'; 

export default function SchematicPage(props: PageProps){
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