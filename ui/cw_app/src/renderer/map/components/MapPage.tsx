// Our Map Page details exists here
import * as styles from '../css/MapPage.module.css';
import BaseLayout from '../../core/components/BaseLayout';
import Map from './Map'; 


export default function MapPage() {

    return (
        <BaseLayout>
            <div className={styles.pageContainer}>
                <Map/>
            </div>
        </BaseLayout>
    );
}
