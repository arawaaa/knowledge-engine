import { Chip, Group, Button, Container, Text, Stack, Checkbox, Title, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useState } from 'react';

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
      <form onSubmit={form.onSubmit((values) => console.log(values))}>
        <Stack>
          <Title order={1}>
            Create your tool-using assistant
          </Title>
          <TextInput
            {...form.getInputProps('name')}
            key={form.key('name')}
            label="Name"
            placeholder="Your Name"
          />
          <TextInput
            {...form.getInputProps('cbotName')}
            key={form.key('cbotName')}
            label="Chatbot's Name"
            placeholder="Name"
          />
          <Checkbox
            {...form.getInputProps('friendly', { type: 'checkbox' })}
            key={form.key('friendly')}
            label="Chatbot should be friendly"
          />
          <Chip.Group multiple {...form.getInputProps('type')} key={form.key('type')}>
            <Group>
              <Text>What should the bot be to you?</Text>
              <Chip value="pr">Programmer</Chip>
              <Chip value="fr">Friend</Chip>
              <Chip value="pl">Planner</Chip>
            </Group>
          </Chip.Group>
          <Group justify="flex-end">
            <Button type="submit">Create</Button>
          </Group>
        </Stack>
      </form>
    </Container>
  );
}
