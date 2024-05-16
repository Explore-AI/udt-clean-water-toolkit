// Our Map Page details exists here
import * as styles from '../css/MapPage.module.css';
import BaseLayout from '../../core/components/BaseLayout';
import MapView from './Map';
import MapContextProvider from '../context/MapContextProvider';

export default function MapPage() {
    return (
        <BaseLayout>
            <MapContextProvider>
                <div className={styles.pageContainer}>
                    <MapView />
                </div>
            </MapContextProvider>
        </BaseLayout>
    );
}
