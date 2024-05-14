import Header from './Header';
import React from 'react'; 

type childrenProps = {
    children: React.ReactNode
}

export default function BaseLayout(props: childrenProps) {

    return (
        <>
            <Header />
            { props.children }
        </>
    );
}
