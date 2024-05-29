import styles from '../css/EdgeNode.module.css'
import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';

export default memo(({ id }) => {

    return (
        <>
            <div className={styles.node} style={{ visibility: 'hidden'}}>
                {/* <div className={styles.label}>
                    {id}
                    </div> */}
            </div>
            <Handle type="source"
                position={Position.Top}
                style={{ visibility: 'hidden', top: '13px', bottom: '0px', left: '3px', right: '0px', width: '1px', height: '1px', border: '0px', maxHeight:'1px', minHeight:'1px', maxWidth:'1px', minWidth:'1px'}}
            />
            <Handle
                type="target"
                position={Position.Top}
                style={{ visibility: 'hidden', top: '13px', bottom: '0px', left: '3px', right: '0px', width: '1px', height: '1px', border: '0px', maxHeight:'1px', minHeight:'1px', maxWidth:'1px', minWidth:'1px'}}
            />
        </>
    );
});
