// use this to create the schematic view
import 'reactflow/dist/base.css';
import '@mantine/dates/styles.css';
import { useContext } from 'react';
import LoadingSpinner from '../../core/components/LoadingSpinner';
import styles from '../css/Schematic.module.css';
import AssetNode from './AssetNode';
import PipeEdgeNode from './PipeNode';
import ReactFlow, { Controls, Node } from 'reactflow';
import useElkLayout from '../hooks/useElkLayout';
import useGetData from '../../core/hooks/useGetData';
import { SchematicUiContext } from '../hooks/useSchematicUi';
import { SchematicProps } from '../types/types';
import { DMA__QUERY_KEY, TRUNKMAIN_QUERY_KEY } from '../queries';
import { isEmpty as _isEmpty, union as _union } from 'lodash';
import MultiSelectField from '../../core/components/MultiSelectField';
import useGetItems from '../../core/hooks/useGetItems';
import { useNavigate } from 'react-router-dom';
import { DateTimeInput } from '../../core/components/DateTimePicker';

const nodeTypes = {
    assetNode: AssetNode,
    pipeNode: PipeEdgeNode,
};

function Schematic() {
    const { queryValues } = useGetData(TRUNKMAIN_QUERY_KEY);
    const { data, isPending, isSuccess } = queryValues;
    const { data: layoutData } = useElkLayout(
        (data as SchematicProps) || { nodes: [], edges: [] },
    );
    const { items, setFilterParams } = useGetItems(DMA__QUERY_KEY);
    const navigate = useNavigate();
    const { nodePopupIds, setSchematicUiParams } =
        useContext(SchematicUiContext);

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
    const onNodeClick = (e: React.MouseEvent, node: Node) => {
        setSchematicUiParams({
            nodePopupIds: _union(nodePopupIds || [], [node.id]),
        });
    };

    const onSearchChange = (value: string) => {
        console.log('[s] value change');
        setFilterParams(DMA__QUERY_KEY, { search: value });
    };

    const onFilterByDmas = (options) => {
        navigate(`/schematic/${options.join('-')}`);
    };

    console.log('[s] data returned: ', data);

    return (
        <>
            <div className={styles.controlHeader}>
                <div className={styles.searchBox}>
                    <MultiSelectField
                        labelName="code"
                        clearable={true}
                        onEnter={onFilterByDmas}
                        onSearchChange={onSearchChange}
                        placeholder="Select the DMA"
                        searchable={true}
                        data={items}
                        maxValues={1}
                    />
                </div>
                <div className={styles.dateTimePicker}>
                    <DateTimeInput /> 
                </div>
            </div>
            <ReactFlow
                nodes={layoutData?.nodes}
                edges={layoutData?.edges}
                nodeTypes={nodeTypes}
                minZoom={0}
                maxZoom={50}
                zoomOnScroll={true}
                fitView={true}
                nodesDraggable={true}
                className={styles.rfContainer}
                onNodeClick={onNodeClick}
            >
                <Controls />
            </ReactFlow>
        </>
    );
}

export default Schematic;
