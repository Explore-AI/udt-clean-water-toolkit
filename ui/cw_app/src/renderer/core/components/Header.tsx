import { useLocation } from 'react-router-dom'
import { map as _map } from 'lodash'
import { Burger } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Link } from 'react-router-dom';
import WaterLogo from '../images/water.svg';
import styles from '../css/Header.module.css';
import { startsWith as _startsWith } from 'lodash'

const links = [
    { path: '/map', label: 'Map' },
    { path: '/graph', label: 'Graph' },
    { path: '/explorer', label: 'Explorer' },
    { path: '/spatial-graph', label: 'Spatial Graph' },
    { path: '/schematic', label: 'Schematic' },
    { path: '/assets', label: 'Assets'},
    { path: '/analysis', label: 'Analysis' },
];

export default function Header() {
    const [opened, { toggle }] = useDisclosure(false);

    const { pathname } = useLocation()

    const linkButtons = _map(links, (link) => (
        <Link
            key={link.label}
            to={link.path}
            className={styles.mainLink}
            data-active={ _startsWith(pathname, link.path) || undefined }>
            {link.label}
        </Link>
    ));

    return (
        <>
            <div className={styles.header}>
                <div className={styles.titleBlock}>
                    <img
                        src={WaterLogo}
                        alt="Water Logo"
                        className={styles.logo}
                        width={30}
                    />
                    <h3> Unlocking Digital Twins POC </h3>
                </div>
                <div className={styles.links}>{linkButtons}</div>
                <div className={styles.menuBlock}>
                    <Burger opened={opened} onClick={toggle} size="sm" />
                    {opened && (
                        <div className={styles.burgerMenu}>
                            <p>Close App Here</p>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}
