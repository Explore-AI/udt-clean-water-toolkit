import { Handle, Position } from 'reactflow';
import { useMemo, memo } from 'react';


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


export default memo(() => {
    return (
        <>
            <Handle type="target" position={Position.Top} style={{ visibility: 'hidden', ...handleStyle}}/>
            <Handle type="source" position={Position.Top} style={{ visibility: 'hidden', ...handleStyle}}/>
        </>
    );
});

// export { PipeEdgeNode };
