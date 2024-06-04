import { Position, Handle } from 'reactflow';

const AssetNode = () => {
    return (
        <>
            <Handle type="target" position={Position.Top}>
                {' '}
            </Handle>
            <Handle type="source" position={Position.Top}>
                {' '}
            </Handle>
        </>
    );
};

export default AssetNode; 

