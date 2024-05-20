import BaseLayout from '../../core/components/BaseLayout';

export default function GraphPage() {
    return (
        <BaseLayout>
            <iframe
                src="http://localhost:7475/"
                title="neo4j browser"
                frameBorder="0"
                style={{ overflow: 'hidden', height: '100vh', width: '100%' }}
            ></iframe>
        </BaseLayout>
    );
}
