import { useContext, memo } from 'react'
import { SchematicUiContext } from '../hooks/useSpatialGraphUi'
import { compact as _compact, map as _map } from 'lodash'
import { AssetPopup } from './AssetPopup';

const NodePopups = (props) => {
    const { properties: nodeProperties } = props

    const { nodePopups, setSchematicUiParams } = useContext(SchematicUiContext)

    const onClosePopup = (nodeId) => {
        const newNodePopups = _map(nodePopups, (node) => {
            if (node.id != nodeId) {
                return node
            }
        });
        setSchematicUiParams({ nodePopups: _compact(newNodePopups) })
    }

    return (
        <>
            { _map(nodePopups, (node) => (
                <div
                    key={node.id}
                    style={{ position: 'relative',
                             zIndex: 5,
                             transform: `translate(${node.position[0]}px, ${node.position[1]-20}px)` }}>
                    <AssetPopup
                        nodeProps={node.properties}
                        onClose={() => onClosePopup(node.id)}
                    />
                </div>
              ))}
        </>
    );
};


export default memo(NodePopups)
