import BaseLayout from '../../core/components/BaseLayout';
import AnalysisForm from './AnalysisForm';
import AnalysisTable from './AnalysisTable'
import { SubmitHandler } from 'react-hook-form';
import styles from '../css/AnalysisPage.module.css';

export default function AnalysisPage() {
    const onSubmit: SubmitHandler<Inputs> = (data) => console.log(data);

    return (
        <BaseLayout>
            <div className={styles.main}>
                <div className={styles.table}>
                    <AnalysisTable/>
                </div>
                <div className={styles.form}>
                    <AnalysisForm onSubmit={onSubmit} />
                </div>
            </div>
        </BaseLayout>
    );
}
