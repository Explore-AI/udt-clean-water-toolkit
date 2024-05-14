// Our Map Page details exists here
import styles from '../css/MapPage.module.css';
import MapLayout from '../../core/components/MapLayout';
import Map from './Map'

export default function MapPage() {

    return (
      <MapLayout>
        <div className={styles['page-container']}>
          <Map/>
        </div>
      </MapLayout>
    );
}
