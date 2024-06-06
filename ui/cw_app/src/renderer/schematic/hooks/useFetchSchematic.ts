import { getBaseUrl } from '../../core/utils';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { SchematicProps } from '../types/types';

const requestData = async (url: string): Promise<SchematicProps> => {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (err) {
        throw new Error(' Error Fetching Data ');
    }
};

const useFetchSchematicData = (queryKey: string[], options = {}) => {
    /**
     * Custom Hook for fetching the trunk main schematic data from our API
     */

    const url = getBaseUrl(queryKey);
    const schematicData = useQuery({
        queryKey: queryKey,
        retry: 0,
        queryFn: async () => {
            let response = await requestData(url);
            return response;
        },
    });

    return schematicData;
};

export default useFetchSchematicData;
