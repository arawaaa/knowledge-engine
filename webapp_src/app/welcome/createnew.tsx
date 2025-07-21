import { Chip, Group, Button, Text, Stack, Checkbox, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';

export function CreateBot() {
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
        <form onSubmit={form.onSubmit((values) => console.log(values))}>
            <Stack>
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
    )
}
