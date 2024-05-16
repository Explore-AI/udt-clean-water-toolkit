import { MantineProvider } from '@mantine/core';
import BaseRouter from './BaseRouter'
import '@mantine/core/styles.css';

function BasePage() {

  return (
    <MantineProvider>
      <BaseRouter/>
    </MantineProvider>
  );
}

export default BasePage;
