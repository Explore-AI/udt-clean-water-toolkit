// Our Map Page details exists here
import styles from '../css/MapPage.module.css';
import withMap from '../hocs/withMap'
import MapView from './MapView';
import BaseLayout from '../../core/components/BaseLayout';

function MapPage() {
    return (
        <BaseLayout>
            <div className={styles.pageContainer}>
                <MapView />
            </div>
        </BaseLayout>
    );
}

export default withMap(MapPage);
