// Our Map Page details exists here
import styles from '../css/MapPage.module.css';
import MapView from './Map';
import MapContextProvider from '../context/MapContextProvider';
import MapLayout from '../../core/components/MapLayout';

export default function MapPage() {
    return (
        <MapLayout>
            <MapContextProvider>
                <div className={styles.pageContainer}>
                    <MapView />
                </div>
            </MapContextProvider>
        </MapLayout>
    );
}
