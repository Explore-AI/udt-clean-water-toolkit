import { useEffect } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { getBaseUrl } from '../utils'

const useFetchJson = (queryKey, options={}) => {

    const url = getBaseUrl(queryKey, options.params)

    const queryValues = useQuery({
        queryKey: [queryKey],
        retry: 0,
        queryFn: async ({ signal }) => {
            const res = await fetch(url, { signal }) //TODO: replace with axios
            return await res.json();
        }
    })

return queryValues
}

export default useFetchJson
