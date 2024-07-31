import styles from '../css/Circle.module.css';
import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { getIcons } from '../../schematic/components/IconComponents';
import { includes as _includes } from 'lodash'

const pipeLabels = ['PipeJunction', 'PipeEnd']


const CircleNode = (props) => {

    const { data } = props

    const assetIcon = data?.label
                    ? getIcons(data?.label)
                    : null;

    //console.log(data.label, "a")

    return (
        <>
            {_includes(pipeLabels, data?.label) &&
             <div className={styles.node}>
             </div>
            }
            {!_includes(pipeLabels, data?.label) &&
             <div className={styles.node}>
             </div>
            }
            <Handle
                type="source"
                position={Position.Top}
                style={{
                    visibility: 'hidden',
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
                }}
            />
            <Handle
                type="target"
                position={Position.Top}
                style={{
                    visibility: 'hidden',
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
                }}
            />
        </>
    );
};
//style={{ visibility: 'hidden', top: '7px', bottom: '0px', left: '10px', right: '0px'}}

//style={{ visibility: 'hidden', width: '1px', height: '1px'}}

//style={{ visibility: 'hidden', top: '10px', bottom: '0px', left: '5px', right: '0px', width: '1px', height: '1px'}}

/* const style = { visibility: 'hidden', top: '14px', bottom: '0px', left: '0px', right: '0px', width: '1px', height: '1px', border: '0px', maxHeight:'1px', minHeight:'1px', maxWidth:'1px', minWidth:'1px'} */


export default memo(CircleNode)
