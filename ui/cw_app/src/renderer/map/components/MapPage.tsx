// Our Map Page details exists here
import styles from '../css/MapPage.module.css';
import withMap from '../hocs/withMap';
import MapView from './MapView';


const MapPage = (props) => {

    const { pageVisibility } = props

    return (
        <div className={styles.pageContainer}
            style={{ display: pageVisibility }}>
            <MapView />
        </div>
    );
}

export default withMap(MapPage);
