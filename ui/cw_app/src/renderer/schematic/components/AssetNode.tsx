import { Position, Handle, NodeProps } from 'reactflow';
import { memo } from 'react';
import { Node } from '../types/types';
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
const nodeStyle = {
    backgroundColor: '#cfeef4',
    width: '100px',
    height: '50px',
    borderRadius: '20%',
    border: '2px solid #393939',
    display: 'inline-block',
};

const AssetNode = memo(() => {
    return (
        <>
            <div style={nodeStyle}></div>
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

export { AssetNode };
