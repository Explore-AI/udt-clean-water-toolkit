import { useQuery } from '@tanstack/react-query';
import useFilterParams from './useFilterParams'

const useGetData = (queryKey) => {

    const { filterParams, setFilterParams } = useFilterParams(queryKey)

    const queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        enabled: false
    })

    return { queryValues, setFilterParams }
}

export default useGetData
