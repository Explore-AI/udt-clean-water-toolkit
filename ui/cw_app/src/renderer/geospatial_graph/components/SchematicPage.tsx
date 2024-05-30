import styles from '../css/SchematicPage.module.css';
import BaseLayout from '../../core/components/BaseLayout';
import Schematic from './Schematic';
import { useQuery } from '@tanstack/react-query';
import { DRF_API_URL } from '../../config';
import { Loader } from '@mantine/core';

/* *
 *     const neo4jNodes = async() => {
 *     const res = await axios.get('http://localhost:8000/cw_graph/neo4j?dma_code=ZCHIPO01')
 *     return [res.data.nodes, res.data.edges]
 * } 
 * */

export default function SchematicPage() {
    const { isPending, error, data } = useQuery({
        queryKey: ['repoData'],
        queryFn: () =>
            fetch(`${DRF_API_URL}cw_graph/schematic/?dma_code=ZCHIPO01`).then(
                (res) => res.json(),
            ),
    });

    let content;
    if (isPending)
        content = (
            <div
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyItems: 'center',
                    padding: '5px',
                    marginTop: '5px', 
                }}
            >
                <Loader color="#35c3da" />
                <p>Loading...</p>
            </div>
        );

    if (error) content = <div>{'An error has occurred: ' + error.message}</div>;

    if (data) content = <Schematic nodes={data.nodes} edges={data.edges} />;

    return (
        <BaseLayout>
            <div className={styles.pageContainer}>{content}</div>
        </BaseLayout>
    );
}
