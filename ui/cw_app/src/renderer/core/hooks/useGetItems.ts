import { useQuery } from '@tanstack/react-query';
import useFilterParams from './useFilterParams'

const useGetItems = (queryKey) => {

    const { filterParams, setFilterParams } = useFilterParams(queryKey)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        enabled: false
    })

    return { items: queryValues.data?.items, pagination: queryValues.data?.pagination, setFilterParams, ...queryValues }
}

export default useGetItems
