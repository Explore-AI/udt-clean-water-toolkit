import { useQuery, useQueryClient } from '@tanstack/react-query';
import useFilterParams from './useFilterParams'
import { getApiUrl } from '../utils/http'
import axios from 'axios'

const requestData = async (url: string, params = {}) => {
    try {
        const response = await axios.get(url, { params });
        return response.data;
    } catch (err) {
        throw new Error(' Error Fetching Data ');
    }
};


const useFetchJson = (queryKey, options={}) => {

    const { filterParams, setFilterParams } = useFilterParams(queryKey, options.params)

    const url = getApiUrl(queryKey, filterParams)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        retry: 0,
        queryFn: () => {
            return requestData(url, options)
        }
    })

    return { queryValues, setFilterParams }
}

export default useFetchJson
