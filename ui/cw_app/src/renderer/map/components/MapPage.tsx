// Our Map Page details exists here
import styles from '../css/MapPage.module.css';
import BaseLayout from '../../core/components/BaseLayout';

export default function MapPage() {

    return (
        <BaseLayout>
            <div className={styles['page-container']}>
                <Map>
            </div>
        </BaseLayout>
    );
}
