import { useQuery } from '@tanstack/react-query';
import useFilterParams from './useFilterParams'

const useGetItems = (queryKey) => {

    const { filterParams, setFilterParams } = useFilterParams(queryKey)
    console.log(filterParams, "uuuuu")
    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        enabled: false
    })

    return { items: queryValues.data?.items, pagination: queryValues.data?.pagination, setFilterParams }
}

export default useGetItems
