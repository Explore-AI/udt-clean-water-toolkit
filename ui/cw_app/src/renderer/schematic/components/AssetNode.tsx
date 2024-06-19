import { Position, Handle, NodeProps } from 'reactflow';
import { memo } from 'react';
import { Node } from '../types/types';
import styles from '../css/AssetNode.module.css';
import { getIcons } from './IconComponents';

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

export default memo((props: NodeProps<Node>) => {
    const { data } = props;
    const { properties: nodeProperties } = data;
    
    const assetIcon = nodeProperties?.asset_names
        ? getIcons(nodeProperties?.asset_names[0])
        : getIcons('default');

    return (
        <>
            <div className={styles.nodeContainer}>
                <div className={styles.containerTitle}>
                    <div className={styles.icon}>{assetIcon}</div>
                    <div className={styles.text}>
                        <strong>{nodeProperties?.label}</strong>
                    </div>
                    <div className={styles.idText}>
                        {nodeProperties?.asset_gids
                            ? nodeProperties?.asset_gids[0]
                            : data.key}
                    </div>
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
        </>
    );
});
