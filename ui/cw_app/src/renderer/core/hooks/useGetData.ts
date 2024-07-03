import { useQuery } from '@tanstack/react-query';
import useFilterParams from './useFilterParams'
import { isEmpty as _isEmpty } from 'lodash'

const useGetData = (queryKey) => {

    const { filterParams, setFilterParams } = useFilterParams(queryKey)

    let queryValues = useQuery({
        queryKey: [queryKey, filterParams],
        enabled: false
    })

    if (_isEmpty(queryValues)) {
       queryValue = { data: [] }
    }

    return { queryValues, setFilterParams }
}

export default useGetData
