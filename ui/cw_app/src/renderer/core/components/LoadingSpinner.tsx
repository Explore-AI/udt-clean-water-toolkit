import styles from '../css/loading-spinner.module.css';
import { Loader } from '@mantine/core';

const LoadingSpinner = () => {

    // TODO: Centre in page
    return (
        <div
            className={styles.spinner}>
            <Loader color="#35c3da" />
            <p>Loading...</p>
        </div>
    );


}

export default LoadingSpinner
