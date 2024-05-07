import { Autocomplete, Group, Burger, rem } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import WaterLogo from '../../../../assets/water.svg';
// import styles from './Header.module.css';

const links = [
  { link: '/', label: 'Home' },
  { link: '/graph', label: 'Graph' },
  { link: '/geo-graph', label: 'Geospatial Graph' },
  { link: '/schematic', label: 'Schematic' },
  { link: '/analysis', label: 'Analysis' },
];

export default function Header() {
  return (
    <>
      <header >
        <p>Your header bar here!</p>
      </header>
    </>
  );
}
