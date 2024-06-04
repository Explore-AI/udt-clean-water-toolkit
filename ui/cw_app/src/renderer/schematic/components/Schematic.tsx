// use this to create the schematic view
import React from 'react';
import LoadingSpinner from '../../core/components/LoadingSpinner';
import useGetSchematicData from '../hooks/useGetSchematicData';

import { TRUNKMAIN_QUERY_KEY } from '../queries';
import { isEmpty as _isEmpty } from 'lodash';
import styles from '../css/Schematic.module.css';
import useFetchSchematicData from '../hooks/useFetchSchematic';

const Schematic = () => {
    console.log('URL: ', TRUNKMAIN_QUERY_KEY);
    const { data, isPending, isSuccess, isError } = useFetchSchematicData([
        TRUNKMAIN_QUERY_KEY,
    ]);

    if (isPending) return <LoadingSpinner />;

    if (_isEmpty(data) && isSuccess) {
        return (
            <div>
                <h1>No data found</h1>
            </div>
        );
    }

    console.log('your data is here: ', data);

    return (
        <>
            <div className={styles.contents}>
                <h1> Schematic View</h1>
                <h2> A schematic diagram comes over here </h2>
            </div>
        </>
    );
};

export default Schematic;
