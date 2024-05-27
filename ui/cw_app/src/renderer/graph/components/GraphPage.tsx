import BaseLayout from '../../core/components/BaseLayout';
import { NEO4J_BROWSER_CONFIG } from '../../config'

export default function GraphPage() {
    return (
        <BaseLayout>
            <iframe
                src={NEO4J_BROWSER_CONFIG}
                title="neo4j browser"
                frameBorder="0"
                style={{ overflow: 'hidden', height: '100vh', width: '100%' }}
            ></iframe>
        </BaseLayout>
    );
}
