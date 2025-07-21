import { AppShell, Text, Group, Image, AspectRatio } from "@mantine/core";
import classes from './header.module.css';

import logo from "./resources/icon.png";

export function Header() {
    return (
        <AppShell.Header>
            <Group className={classes.paddedBox}>
                <AspectRatio flex="0 0 40px">
                    <Image src={logo}/>
                </AspectRatio>
                <Text size="lg">Agent Chat</Text>
            </Group>
        </AppShell.Header>
    )
}
