import { useState } from 'react';
import { Container,Group, Burger, Box } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Link } from 'react-router-dom';
import WaterLogo from '../../../../assets/water.svg';
import styles from './Header.module.css';

const links = [
    { link: '/', label: 'Home' },
    { link: '/graph', label: 'Graph' },
    { link: '/geo-graph', label: 'Geospatial Graph' },
    { link: '/schematic', label: 'Schematic' },
    { link: '/analysis', label: 'Analysis' },
];

export default function Header() {
    const [opened, { toggle }] = useDisclosure(false);
    const [active, setActive] = useState(0);

    const items = links.map((link, index) => (
        <Link
            key={link.label}
            to={link.link}
            className={styles.mainLink}
            data-active={index === active || undefined}
            onClick={() => {
                setActive(index);
            }}
        >
            {link.label}
        </Link>
    ));

    return (
        <>
            <header className={styles.header}>
                <Container className={styles.inner}>
                    <Group>
                        <img src={WaterLogo} alt="Water Logo" width={30} />
                        <p> Clean Water Application </p>
                    </Group>
                    <Box visibleFrom="sm" className={styles.links}>
                        <Group gap={1} className={styles.mainLinks}>
                            {items}
                        </Group>
                    </Box>

                    <Burger
                        opened={opened}
                        onClick={toggle}
                        className={styles.burger}
                        size="sm"
                        hiddenFrom="sm"
                    />
                </Container>
            </header>
        </>
    );
}
