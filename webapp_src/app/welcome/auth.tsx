import { Container, Title, Stack, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'


type auth = {
    usr: string;
    pwd: string;
}

export function Auth({}) {
    const form = useForm<auth>({
        mode: "uncontrolled",
        initialValues: {
            usr: "",
            pwd: ""
        }
    })
    return (
        <Container>
            <Title order={1}> Sign Up / Log In to continue </Title>
            <form>
                <Stack>
                    <TextInput {...form.getInputProps('usr')} label="Username:" placeholder="Username" />
                    <TextInput {...form.getInputProps('pwd')} label="Password:" placeholder="Password" />
                </Stack>
            </form>
        </Container>
    )
}
