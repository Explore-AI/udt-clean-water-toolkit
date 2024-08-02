import styles from '../css/graph-page.css'
import { NEO4J_BROWSER_CONFIG } from '../../config'

const GraphPage = (props) => {

    const { pageVisibility } = props

    return (
        <div className={pageVisibility}>
            <iframe
                src={NEO4J_BROWSER_CONFIG}
                title="neo4j browser"
                frameBorder="0">
            </iframe>
        </div>
    );
}

export default GraphPage
