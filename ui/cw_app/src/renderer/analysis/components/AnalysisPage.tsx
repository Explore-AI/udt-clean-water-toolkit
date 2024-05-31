import styles from '../css/AnalysisPage.module.css';
import AnalysisForm from './AnalysisForm';
import AnalysisTable from './AnalysisTable'
import { SubmitHandler } from 'react-hook-form';


const AnalysisPage = (props) => {

    const { pageVisibility } = props


    const onSubmit: SubmitHandler<Inputs> = (data) => console.log(data);

    return (
        <div className={styles.main} style={{ display: pageVisibility }}>
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
