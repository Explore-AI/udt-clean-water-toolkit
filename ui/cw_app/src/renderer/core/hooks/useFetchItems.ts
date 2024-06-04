import { useQuery, useQueryClient } from '@tanstack/react-query';
import useSetFilterParams from './useSetFilterParams'
import { getBaseUrl } from '../utils'

const useFetchItems = (queryKey, options={}) => {

    const filterParams = useSetFilterParams(queryKey, options.params)

    const url = getBaseUrl(queryKey, options.params)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        retry: 0,
        queryFn: async ({ signal }) => {
            let res = await fetch(url, { signal }) //TODO: replace with axios
            res = await res.json();
            return { items: res.items, pagination: res.pagination }
        }
    })

    return queryValues
}

export default useFetchItems
