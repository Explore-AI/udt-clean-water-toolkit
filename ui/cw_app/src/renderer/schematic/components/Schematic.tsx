// use this to create the schematic view
import 'reactflow/dist/base.css';
import '../css/schematic.css';
import styles from '../css/Schematic.module.css';
import { useContext } from 'react'
import LoadingSpinner from '../../core/components/LoadingSpinner';
import MultiSelectField from '../../core/components/MultiSelectField'
import AssetNode from './AssetNode';
import PipeEdgeNode from './PipeEdgeNode';
import PipeNode from './PipeNode';
import ReactFlow, { Controls, Node } from 'reactflow';
import useElkLayout from '../hooks/useElkLayout';
import useGetData from '../../core/hooks/useGetData';
import useGetItems from '../../core/hooks/useGetItems'
import NodePopups from './NodePopups'
import { useNavigate } from 'react-router-dom';
import { SchematicUiContext } from '../hooks/useSchematicUi'
import { SchematicProps } from '../types/types';
import { TRUNKMAIN_QUERY_KEY } from '../queries';
import { isEmpty as _isEmpty, union as _union } from 'lodash';

const nodeTypes = {
    assetNode: AssetNode,
    pipeNode: PipeNode,
    pipeEdgeNode: PipeEdgeNode,
};

const DMA__QUERY_KEY = 'cw_utilities/dma'

function Schematic() {

    const navigate = useNavigate();

    const { queryValues } = useGetData(TRUNKMAIN_QUERY_KEY);
    const { data, isPending, isSuccess } = queryValues
    const { data: layoutData } = useElkLayout(data as SchematicProps || { nodes: [], edges: [] });

    const { items, setFilterParams } = useGetItems(DMA__QUERY_KEY)

    const { nodePopupIds, setSchematicUiParams } = useContext(SchematicUiContext)

    const onNodeClick = (
        e: React.MouseEvent,
        node: Node,
    ) => {
        setSchematicUiParams({ nodePopupIds: _union(nodePopupIds || [], [node.id])});
    };


    const onNodeClick2 = (
        e: React.MouseEvent,
        node: Node,
    ) => {
        setSchematicUiParams({
            nodePopups: [
                {
                    id: node.id,
                    data: node.data,
                    position: [e.clientX, e.clientY]
                }
            ]
        });
    };

    if (isPending) {
            return <LoadingSpinner />;
    }

    if (_isEmpty(data) && isSuccess) {
        return (
            <div>
                <h1>No data found</h1>
            </div>
        );
    }


    const onSearchChange = (value) => {
        setFilterParams(DMA__QUERY_KEY, { search: value })
    }

    const onFilterByDmas = (options) => {
        navigate(`/spatial-graph/${options.join("-")}`);
    }
    //fitView={true}
    //nodesDraggable={true}
    return (
        <>
            <div className={styles['search_box']}>
                <MultiSelectField
                    labelName="code"
                    clearable={true}
                    onEnter={onFilterByDmas}
                    onSearchChange={onSearchChange}
                    searchable={true}
                    placeholder="Search by DMA"
                    data={items} />
            </div>
            <ReactFlow
                nodes={layoutData?.nodes}
                edges={layoutData?.edges}
                nodeTypes={nodeTypes}
                minZoom={0}
                maxZoom={50}
                zoomOnScroll={true}
                className={styles.rfContainer}
                onNodeClick={onNodeClick2}>
                <Controls />
                <NodePopups/>
            </ReactFlow>
        </>
    );
}

export default Schematic;
