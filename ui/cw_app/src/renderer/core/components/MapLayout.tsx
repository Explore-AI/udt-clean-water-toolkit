import { Outlet } from 'react-router-dom';
import Header from './Header';
import React from 'react';

type childrenProps = {
    children: React.ReactNode
}

export default function MapLayout(props: childrenProps) {

    return (
      <>
        <Header />
          { props.children }
      </>
    );
}
