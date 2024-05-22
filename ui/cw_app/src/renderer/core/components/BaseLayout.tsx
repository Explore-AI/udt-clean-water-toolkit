import Header from './Header';
import React from 'react';
import styles from '../css/base_layout.module.css'

type childrenProps = {
    children: React.ReactNode
}

export default function BaseLayout(props: childrenProps) {

    return (
      <>
        <Header />
        <div className={styles['page_block']}>
          { props.children }
        </div>
      </>
    );
}
