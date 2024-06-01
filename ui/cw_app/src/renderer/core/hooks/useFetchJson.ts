import { useQuery } from '@tanstack/react-query';
import * as http from '../utils'

const useFetchJson = (queryKey, options={}) => {
    console.log(queryKey)
    const url = http.getBaseUrl(queryKey, options.params)
    console.log(url, "oooooo")
    const { isPending, error, data } = useQuery({
        queryKey: [queryKey],
        queryFn: async ({ signal }) =>  {
            const res = await fetch(url, { signal }) //TODO: replace with axios
            return await res.json();
    }})

    return { isPending, error, data }
}

export default useFetchJson
