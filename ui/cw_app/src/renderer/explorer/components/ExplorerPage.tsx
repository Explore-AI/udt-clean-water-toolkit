import '../css/explorer-page.css'

const ExplorerPage = (props) => {

    const { pageVisibility } = props

    return (
        <div className={pageVisibility}>
            <iframe
                src='https://www.yworks.com/neo4j-explorer/'
                title="explorer browser"
                frameBorder="0">
            </iframe>
        </div>
    );
}

export default ExplorerPage
