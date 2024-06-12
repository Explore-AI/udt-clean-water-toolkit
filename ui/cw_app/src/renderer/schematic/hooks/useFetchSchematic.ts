import { getApiUrl } from '../../core/utils/http';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { SchematicProps } from '../types/types';

const requestData = async (url: string, params = {}): Promise<SchematicProps> => {
    try {
        const response = await axios.get(url, { params });
        return response.data;
    } catch (err) {
        throw new Error(' Error Fetching Data ');
    }
};

const useFetchSchematicData = (queryKey: string[], options = {}) => {
    /**
     * Custom Hook for fetching the trunk main schematic data from our API
     */
    console.log(options); 
    const url = getApiUrl(queryKey);
    const schematicData = useQuery({
        queryKey: queryKey,
        retry: 0,
        queryFn: async () => {
            let response = await requestData(url, options);
            return response;
        },
    });

    return schematicData;
};

export default useFetchSchematicData;
