import { useQuery } from '@tanstack/react-query';
import useGetFilterParams from './useGetFilterParams'

const useGetItems = (queryKey) => {

    const filterParams = useGetFilterParams(queryKey)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        enabled: false
    })

    return { items: queryValues.data?.items, pagination: queryValues.data?.pagination }
}

export default useGetItems
