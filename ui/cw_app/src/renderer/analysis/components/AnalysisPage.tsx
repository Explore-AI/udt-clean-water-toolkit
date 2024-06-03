import styles from '../css/analysis-page.module.css';
import AnalysisForm from './AnalysisForm';
import AnalysisTable from './AnalysisTable'
import { SubmitHandler } from 'react-hook-form';


const AnalysisPage = (props) => {

    const { pageVisibility } = props

    const mainCss = `${styles.main} ${styles[pageVisibility]}`

    const onSubmit: SubmitHandler<Inputs> = (data) => console.log(data);

    return (
        <div className={mainCss}>
            <div className={styles.table}>
                <AnalysisTable/>
            </div>
            <div className={styles.form}>
                <AnalysisForm onSubmit={onSubmit} />
            </div>
        </div>
    );
}

export default AnalysisPage
