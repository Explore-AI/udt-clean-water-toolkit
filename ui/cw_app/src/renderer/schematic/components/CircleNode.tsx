import React, { memo } from 'react';
import { Handle, useStore, Position } from 'reactflow';

export default memo(({ id }) => {

    return (
        <>
            <div className="dot">
            </div>
            <Handle type="source" position={Position.Left} id="a" style={{ visibility: 'hidden',   height: '0px', width: '0px'}}/>
            <Handle
                type="target"
                position={Position.Right}
                id="b"
                style={{ visibility: 'hidden',   height: '0px', width: '0px'}}
            />
        </>
    );
});
