import { NEO4J_BROWSER_CONFIG } from '../../config'

const GraphPage = (props) => {

    const { pageVisibility } = props

    return (
        <iframe
            src={NEO4J_BROWSER_CONFIG}
            title="neo4j browser"
            frameBorder="0"
            style={{ overflow: 'hidden', height: '100vh', width: '100%', display: pageVisibility }}
        ></iframe>
    );
}

export default GraphPage
