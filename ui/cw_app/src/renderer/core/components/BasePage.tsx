import { MantineProvider } from '@mantine/core';
import BaseRouter from './BaseRouter'

function BasePage() {

  return (
    <MantineProvider>
      <BaseRouter/>
    </MantineProvider>
  );
}

export default BasePage;
