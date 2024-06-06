import { useQuery, useQueryClient } from '@tanstack/react-query';
import useFilterParams from './useFilterParams'
import { getApiUrl } from '../utils/http'

const useFetchJson = (queryKey, options={}) => {

    const { filterParams, setFilterParams } = useFilterParams(queryKey, options.params)

    const url = getApiUrl(queryKey, filterParams)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        retry: 0,
        queryFn: async ({ signal }) => {
            const res = await fetch(url, { signal }) //TODO: replace with axios
            return await res.json();
        }
    })

    return { queryValues, setFilterParams }
}

export default useFetchJson
