import { Chip, Group, Button, Text, Stack, Checkbox, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useContext, useState } from 'react';
import { GlobalCtx } from '~/contexts';
import { Auth } from './auth';
import type { globalState } from '~/contexts';

type CreationValues = {
    name: string;
    cbotName: string;
    friendly: boolean;
    type: Array<string>;
}

function submitValues(values: CreationValues, ctx: globalState) {

}

function BotForm({ moveToLogin } : { moveToLogin: React.Dispatch<React.SetStateAction<boolean>> }) {
    const ctx = useContext(GlobalCtx)
    const form = useForm<CreationValues>({
        mode: "uncontrolled",
        initialValues: {
            name: '',
            cbotName: 'Jemma',
            friendly: true,
            type: Array<string>()
        }
    })

    return (
        <form onSubmit={form.onSubmit((values) => {
            if (ctx?.loggedIn) {
                submitValues(values, ctx)
            } else {
                moveToLogin(true)
            }
        })} >
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

export function CreateBot() {
    const ctx = useContext(GlobalCtx)
    const [loginShown, setLoginShown] = useState<boolean>(false)

    return (
        <>
            {loginShown ? (<Auth />) : (<BotForm moveToLogin={setLoginShown} />)}
        </>
    )
}
