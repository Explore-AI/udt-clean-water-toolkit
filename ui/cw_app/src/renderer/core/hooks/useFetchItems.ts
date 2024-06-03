import { useEffect } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { getBaseUrl } from '../utils'

const useFetchItems = (queryKey, options={}) => {

    const url = getBaseUrl(queryKey, options.params)

    const queryValues = useQuery({
        queryKey: [queryKey],
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
