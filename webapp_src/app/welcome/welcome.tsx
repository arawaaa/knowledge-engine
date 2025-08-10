import { Container, Title} from '@mantine/core';
import { CreateBot } from './createnew';

export function Welcome() {
  return (
    <Container>
      <Title order={1}>
        Create your tool-using assistant
      </Title>
      <CreateBot />
    </Container>
  );
}
