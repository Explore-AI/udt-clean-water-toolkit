import styles from '../css/AssetNode.module.css';
import { useContext, memo } from 'react'
import { Position, Handle, NodeProps } from 'reactflow';
import { Node } from '../types/types';
import { SchematicUiContext } from '../hooks/useSchematicUi'
import { includes as _includes, filter as _filter, map as _map } from 'lodash'
import { AssetPopup } from './AssetPopup';

const NodePopups = (props: NodeProps<Node>) => {
    const { properties: nodeProperties } = props

    const { nodePopupIds, setSchematicUiParams } = useContext(SchematicUiContext)


    const onClosePopup = (nodeId) => {
        const newNodePopupIds = _filter(nodePopupIds, (id) => id != nodeId );
        setSchematicUiParams({ nodePopupIds: newNodePopupIds })
    }

    return (
        <>
            { _map(nodePopupIds, (nodeId) => (
                <AssetPopup
                    nodeProps={nodeProperties}
                    onClose={() => onClosePopup(nodeId)}
                />
              ))}
        </>
    );
};


export default memo(NodePopups)
