import styles from '../css/graph-page.module.css'
import { NEO4J_BROWSER_CONFIG } from '../../config'

const GraphPage = (props) => {

    const { pageVisibility } = props

    return (
        <div className={styles[pageVisibility]}>
            <iframe
                src={NEO4J_BROWSER_CONFIG}
                title="neo4j browser"
                frameBorder="0"
                style={{ width: '100vw', height: '100vh', overflow: 'hidden' }}>
            </iframe>
        </div>
    );
}

export default GraphPage
