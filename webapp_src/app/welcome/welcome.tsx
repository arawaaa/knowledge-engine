import { Chip, Group, Button, Container, Text, Stack, Checkbox, Title, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useState } from 'react';
import { CreateBot } from './createnew';

export function Welcome() {
  const form = useForm({
    mode: "uncontrolled",
    initialValues: {
      name: '',
      cbotName: 'Jemma',
      friendly: true,
      type: Array<string>()
    }
  })

  return (
    <Container>
      <Title order={1}>
        Create your tool-using assistant
      </Title>
      <CreateBot />
    </Container>
  );
}
