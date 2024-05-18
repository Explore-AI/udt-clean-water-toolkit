import React from 'react';
import styles from '../css/BasePopup.module.css';

interface PopupProps {
    children: React.ReactNode;
}

export default function BasePopup({ children }: PopupProps) {
    return <div className={styles.container}>{children}</div>;
}
