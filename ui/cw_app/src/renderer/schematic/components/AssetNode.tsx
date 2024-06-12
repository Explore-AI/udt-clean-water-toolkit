import { Position, Handle, NodeProps } from 'reactflow';
import { memo, useState } from 'react';
import { Node } from '../types/types';
import styles from '../css/AssetNode.module.css';
// import { Default } from './IconComponents/NetworkMeter';
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

const splitAssetName = (name: string) => {
    return name.replace(/_/g, ' ');
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
                    <p>
                        {nodeProperties?.asset_names
                            ? splitAssetName(nodeProperties?.asset_names[0])
                            : 'Point Asset '}
                    </p>
                    <p>  -  </p>
                    <p>
                        {nodeProperties?.asset_gids
                            ? nodeProperties?.asset_gids[0]
                            : data.key}
                    </p>
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
