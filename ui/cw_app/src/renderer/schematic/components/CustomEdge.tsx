import React from 'react';
import {
    BaseEdge,
    EdgeProps,
    getStraightPath,
    useReactFlow,
} from 'reactflow';

export default function CustomEdge({
    id,
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    style = {},
    markerEnd,
}: EdgeProps) {

    const [ edgePath ] = getStraightPath({
        sourceX,
        sourceY,
        targetX,
        targetY,
    });

    console.log(sourceX, sourceY)

    return (
        <BaseEdge path={edgePath} style={style} />
    );
}
