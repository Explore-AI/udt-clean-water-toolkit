import { Outlet } from 'react-router-dom';
import Header from './Header';

export default function BaseLayout(props) {

    return (
        <>
            <Header />
            { props.children }
        </>
    );
}
