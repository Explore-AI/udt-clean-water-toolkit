import { useQuery, useQueryClient } from '@tanstack/react-query';
import useFilterParams from './useFilterParams'
import { getApiUrl } from '../utils/http'

const useFetchItems = (queryKey, options={}) => {

    const { filterParams, setFilterParams } = useFilterParams(queryKey, options.params)

    const url = getApiUrl(queryKey, filterParams)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        retry: 0,
        queryFn: async ({ signal }) => {
            let res = await fetch(url, { signal }) //TODO: replace with axios
            res = await res.json();
            return { items: res.items, pagination: res.pagination }
        }
    })

    return { queryValues, setFilterParams }
}

export default useFetchItems
