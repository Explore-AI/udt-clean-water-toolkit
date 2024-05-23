import React, { memo } from 'react';
import { Handle, useStore, Position } from 'reactflow';

export default memo(({ id }) => {

    return (
        <>
            <div className="dot">
            </div>
            <Handle type="source" position={Position.Left} id="a" />
            <Handle
                type="target"
                position={Position.Right}
                id="b"
            />
        </>
    );
});
