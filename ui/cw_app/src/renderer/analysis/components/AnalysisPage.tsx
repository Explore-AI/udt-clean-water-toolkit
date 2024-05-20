import BaseLayout from '../../core/components/BaseLayout';
import AnalysisForm from './AnalysisForm';
import { SubmitHandler } from 'react-hook-form';
import styles from '../css/analysis_page.module.css';

export default function AnalysisPage() {
    const onSubmit: SubmitHandler<Inputs> = (data) => console.log(data);

    return (
        <BaseLayout>
            <div className={styles['main']}>
                <AnalysisForm onSubmit={onSubmit} />
            </div>
        </BaseLayout>
    );
}
