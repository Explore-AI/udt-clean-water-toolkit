import { useQuery, useQueryClient } from '@tanstack/react-query'
import { get as _get, isEmpty as _isEmpty, isEqual as _isEqual } from 'lodash'

const useFilterParams = (queryKey, params={}) => {

    const { data }  = useQuery({
        queryKey: ['filterParams', queryKey],
        enabled: false
    })

    const currentParams = data

    const queryClient = useQueryClient()

    const setFilterParams = (queryKey, newParams) => {
        const updatedParams = { ...currentParams, ...newParams }
        queryClient.setQueryData(['filterParams', queryKey], updatedParams)
        return updatedParams
    }

    if (!_isEmpty(params) && !_isEqual(params, currentParams)) {
        const filterParams = setFilterParams(queryKey, params)

        return { filterParams, setFilterParams }
    }

    return { filterParams: currentParams, setFilterParams }
}

export default useFilterParams
