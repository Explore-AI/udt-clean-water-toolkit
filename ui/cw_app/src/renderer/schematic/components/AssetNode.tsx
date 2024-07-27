import styles from '../css/AssetNode.module.css';
import { useContext, memo } from 'react'
import { Position, Handle, NodeProps } from 'reactflow';
import { Node } from '../types/types';
import { SchematicUiContext } from '../hooks/useSchematicUi'
import { getIcons } from './IconComponents';
import { includes as _includes, filter as _filter } from 'lodash'
import { AssetPopup } from './AssetPopup';

const handleStyle = {
    top: '13px',
    bottom: '0px',
    left: '3px',
    right: '0px',
    width: '1px',
    height: '1px',
    border: '0px',
    maxHeight: '1px',
    minHeight: '1px',
    maxWidth: '1px',
    minWidth: '1px',
};

const AssetNode = (props: NodeProps<Node>) => {
    const { data, id: nodeId } = props;
    const { properties: nodeProperties } = data;

    const { nodePopupIds, setSchematicUiParams } = useContext(SchematicUiContext)

    const assetIcon = nodeProperties?.label
                    ? getIcons(nodeProperties?.label)
                    : getIcons('default');

    const onClosePopup = (e) => {
        const newNodePopupIds = _filter(nodePopupIds, (id) => id != nodeId );
        setSchematicUiParams({ nodePopupIds: newNodePopupIds })
        e.stopPropagation()

    }

    return (
        <>
            <div className={styles.nodeContainer}>
                <div className={styles.containerTitle}>
                    {assetIcon}
                </div>
            </div>
            <Handle
                type="target"
                position={Position.Top}
                style={{ visibility: 'hidden', ...handleStyle }}
            ></Handle>
            <Handle
                type="source"
                position={Position.Bottom}
                style={{ visibility: 'hidden', ...handleStyle }}
            ></Handle>
            { _includes(nodePopupIds, nodeId) &&
              <AssetPopup
                  nodeProps={nodeProperties}
                  onClose={onClosePopup}
              />
            }
        </>
    );
};


export default memo(AssetNode)
