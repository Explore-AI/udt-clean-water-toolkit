import Header from './Header';
import React from 'react';
import styles from '../css/map_layout.module.css';

type childrenProps = {
    children: React.ReactNode;
};

export default function MapLayout(props: childrenProps) {
    return (
        <div className={styles['page_block']}>
            <Header />
            {props.children}
        </div>
    );
}
