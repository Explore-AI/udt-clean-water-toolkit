import styles from '../css/AnalysisTable.module.css'
import { Table } from '@mantine/core';

const elements = [
    { id: 1, method: 'gis2neo4j', startTime: 'Monday, 11 May, 10:34', name: 'Test 1' },
    { id: 2, method: 'gis2nx', startTime: 'Monday, 11 May, 13:31', name: 'Test 2' },
    { id: 3, method: 'gis2nkj', startTime: 'Monday, 12 May, 11:54', name: 'Test 4' },
    { id: 4, method: 'neo4j2wntrinp', startTime: 'Monday, 13 May, 10:06', name: 'Test 4' },
    { id: 5, method: 'networkcoverage', startTime: 'Monday, 18 May, 09:12', name: 'Test 5'}
];

function AnalysisTable() {

    const rows = elements.map((element) => (
        <Table.Tr key={element.id}>
            <Table.Td>{element.id}</Table.Td>
            <Table.Td>{element.name}</Table.Td>
            <Table.Td>{element.method}</Table.Td>
            <Table.Td>{element.startTime}</Table.Td>
        </Table.Tr>
    ));

    return (
        <div>
            <Table className={}>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>#</Table.Th>
                        <Table.Th>Method</Table.Th>
                        <Table.Th>Name</Table.Th>
                        <Table.Th>Start time</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>{rows}</Table.Tbody>
            </Table>
        </div>
    );
}

export default AnalysisTable
