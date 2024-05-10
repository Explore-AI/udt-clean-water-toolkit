import BaseLayout from '../../core/components/BaseLayout';
import { Image, Text } from '@mantine/core';

export default function GraphViewPage() {
    return (
        <BaseLayout>
            <div className='bg-slate-700'>
                <h1>Graph View Page</h1>
                <Image radius="md" h={200} w={200} src="https://www.svgrepo.com/show/395638/rocket.svg" alt="rocket-ship" />
                <Text className='text-lg text-sky-400/100 border-slate-400 bg-zinc-600'> On the Way to the mooon!</Text>
            </div>
        </BaseLayout>
    );
}
