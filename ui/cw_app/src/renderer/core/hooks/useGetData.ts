import { useQuery } from '@tanstack/react-query';
import useGetFilterParams from './useGetFilterParams'

const useGetData = (queryKey) => {

    const filterParams = useGetFilterParams(queryKey)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        enabled: false
    })

    return queryValues
}

export default useGetData
