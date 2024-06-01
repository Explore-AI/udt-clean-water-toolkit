import { useEffect } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query';
import * as http from '../utils'

const useFetchJson = (queryKey, options={}) => {

    const url = http.getBaseUrl(queryKey, options.params)

    const queryClient = useQueryClient()

    useEffect(() => {
        queryClient.setQueryDefaults([queryKey],  { staleTime: 1000 * 180 })
    }, [])

    const queryValues = useQuery({
        queryKey: [queryKey],
        queryFn: async ({ signal }) => {
            const res = await fetch(url, { signal }) //TODO: replace with axios
            return await res.json();
        }
    })

return queryValues
}

export default useFetchJson
