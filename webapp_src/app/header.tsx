import { AppShell, Text, Button, Group, Image, AspectRatio } from "@mantine/core";
import classes from './header.module.css';
import { useContext } from 'react';
import { GlobalCtx } from './root'
import { useNavigate } from 'react-router'

import logo from "./resources/icon.png";

export function Header() {
    const globalCtx = useContext(GlobalCtx);
    const navigate = useNavigate()

    console.log(globalCtx)
    function buttonPressed() {
        if (globalCtx?.loggedIn) {
            navigate('/home')
        } else {
            navigate('/signup')
        }
    }

    return (
        <AppShell.Header>
            <Group className={classes.paddedBox}>
                <AspectRatio flex="0 0 40px">
                    <Image src={logo}/>
                </AspectRatio>
                <Text size="lg">Agent Chat</Text>
                <Button onClick={(_ev) => buttonPressed()}>
                    {globalCtx?.loggedIn ? "Home" : "Sign Up / Login"}
                </Button>
            </Group>
        </AppShell.Header>
    )
}
