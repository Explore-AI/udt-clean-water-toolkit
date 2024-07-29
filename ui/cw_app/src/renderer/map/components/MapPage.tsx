// Our Map Page details exists here
import 'mapbox-gl/dist/mapbox-gl.css';
import '../css/map-page.css'
import styles from '../css/map-page.module.css';
import withMap from '../hocs/withMap';
import MapView from './MapView';


const MapPage = (props) => {

    const { pageVisibility } = props

    const mainCss = `${styles.pageContainer} ${styles[pageVisibility]}`

    return (
        <div className={mainCss}>
            <MapView />
        </div>
    );
}

export default withMap(MapPage);
