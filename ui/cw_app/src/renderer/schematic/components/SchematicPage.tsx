import BaseLayout from '../../core/components/BaseLayout';
import Schematic from './Schematic'
import {
    useQuery,
} from '@tanstack/react-query'

/* const neo4jNodes = async() => {
 *     const res = await axios.get('http://localhost:8000/cw_graph/neo4j?dma_code=ZCHIPO01')
 *     return [res.data.nodes, res.data.edges]
 * } */

export default function SchematicPage() {

    const { isPending, error, data } = useQuery({
        queryKey: ['repoData'],
        queryFn: () =>
            fetch('http://localhost:8000/cw_graph/schematic/?dma_code=ZCHIPO01').then((res) =>
                res.json(),
            ),
    })

    if (isPending) return 'Loading...'

    if (error) return 'An error has occurred: ' + error.message

    return (
        <BaseLayout>
            <div style={{overflow:'hidden', height:'100vh', width:'100%'}}>
                <Schematic nodes={data.nodes} edges={data.edges} />
            </div>
        </BaseLayout>
    );
}
