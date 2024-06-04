import styles from '../css/AnalysisForm.module.css'
import { useForm, SubmitHandler } from 'react-hook-form';
import { Select, TextInput, NumberInput, Checkbox, MultiSelect, Button } from '@mantine/core';

type Inputs = {
    name: string;
    method: string;
    srid: number,
    offset: number,
    limit: number,
    parallel: boolean,
    processor_count: number,
    batch_size: number
};

type childrenProps = {
    children: React.ReactNode;
};

const METHODS = ["gis2nx",
                 "gis2neo4j",
                 "gis2nk",
                 "neo4j2wntrinp",
                 "neo4j2wntrjson",
                 "neo4j2networkitgraphml",
                 "networkcoverage"]

export default function AnalysisForm(props: childrenProps) {
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors },
    } = useForm<Inputs>();

    const { onSubmit } = props;

    return (
        /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
        <form onSubmit={handleSubmit(onSubmit)}>
            <div className={styles.field}>
                <TextInput
                    label="Run name"
                    placeholder="Input run name"
                    {...register('name')}
                />
            </div>

            <div className={styles.field}>
                <Select
                    label="Method"
                    placeholder="Select method"
                    data={METHODS}
                />
            </div>

            <div className={styles.field}>
                <TextInput
                    label="SRID"
                    placeholder="Input srid"
                    {...register('srid')}
                />
            </div>


            <div className={styles.field}>
                <MultiSelect
                    label="DMA"
                    description="Select the DMAs for study or the 'Entire network'"
                    placeholder="Select DMAs"
                    data={['React', 'Angular', 'Vue', 'Svelte']}
                />
            </div>

            <div className={styles.field}>
                <NumberInput
                    label="Offset"
                    description="Only valid for the gis2neo4j, gis2nx, and gis2nk methods"
                    placeholder="Select query offset"
                    {...register('offset')}
                />
            </div>

            <div className={styles.field}>
                <NumberInput
                    label="Limit"
                    description="Only valid for the gis2neo4j, gis2nx, and gis2nk methods"
                    placeholder="Select query limit"
                    {...register('limit')}
                />
            </div>

            <div className={styles.field}>
                <NumberInput
                    label="Batch size"
                    placeholder="Select batch size"
                    {...register('batch_size')}
                />
            </div>

            <div className={styles.field}>
                <Checkbox
                    defaultChecked={false}
                    label="Multiprocessing enabled"
                    {...register('parallel')}
                />
            </div>

            <div className={styles.field}>
                <NumberInput
                    label="Processor count"
                    description="Only valid for methods that use multiprocessing"
                    placeholder="Select processor count"
                    {...register('processor_count')}
                />
            </div>

            <div className={styles.field}>
                <NumberInput
                    label="Chunk size"
                    description="Only valid for methods that use multiprocessing"
                    placeholder="Select batch size"
                    {...register('chunk_size')}
                />
            </div>

            <div>
                <Button variant="filled" color="green">Run</Button>
            </div>
        </form>
    );
}
