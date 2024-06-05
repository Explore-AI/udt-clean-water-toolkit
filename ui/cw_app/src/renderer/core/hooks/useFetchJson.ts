import { useQuery, useQueryClient } from '@tanstack/react-query';
import useFilterParams from './useFilterParams'
import { getBaseUrl } from '../utils'

const useFetchJson = (queryKey, options={}) => {

    const { filterParams } = useFilterParams(queryKey, options.params)

    const url = getBaseUrl(queryKey, options.params)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        retry: 0,
        queryFn: async ({ signal }) => {
            const res = await fetch(url, { signal }) //TODO: replace with axios
            return await res.json();
        }
    })

    return queryValues
}

export default useFetchJson
