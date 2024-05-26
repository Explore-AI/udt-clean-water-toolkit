import { useState } from 'react';
import { useLocation } from 'react-router-dom'
import { map as _map } from 'lodash'
import { Burger } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Link } from 'react-router-dom';
import WaterLogo from '../images/water.svg';
import styles from '../css/Header.module.css';

const links = [
    { link: '/map', label: 'Map' },
    { link: '/graph', label: 'Graph' },
    { link: '/geo-graph', label: 'Geospatial Graph' },
    { link: '/schematic', label: 'Schematic' },
    { link: '/analysis', label: 'Analysis' },
];

export default function Header() {
    const [opened, { toggle }] = useDisclosure(false);

    const { pathname } = useLocation()

    console.log(pathname, "A")

    const linkButtons = _map(links, (link) => (
        <Link
            key={link.label}
            to={link.link}
            className={styles.mainLink}
            data-active={ pathname === link.link || undefined }>
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
