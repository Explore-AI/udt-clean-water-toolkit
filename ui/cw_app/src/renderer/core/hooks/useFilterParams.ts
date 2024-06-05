import { useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { get as _get, isEmpty as _isEmpty } from 'lodash'

const useFilterParams = (queryKey, params={}) => {

    const allParams = useQuery({
        queryKey: 'filterParams',
        enabled: false
    })

    const currentParams = _get(allParams, `data.${queryKey}`, {})
    console.log(queryKey, currentParams, "aaaa")

    //console.log(allParams.data)

    const [ stateParams, setStateParams ] = useState({})
    console.log(stateParams, "rrrrr")
    const queryClient = useQueryClient()

    //const allParams = queryClient.getQueryData('filterParams')

    //const currentParams = _get(allParams, `${queryKey}`, {})

    const setFilterParams = (queryKey, newParams) => {
        const updatedParams = { ...currentParams, ...newParams }
        queryClient.setQueryData('filterParams', { [queryKey]: updatedParams })
        setStateParams(updatedParams)
        return updatedParams
    }

    if (!_isEmpty(params)) {
        const filterParams = setFilterParams(queryKey, params)
        console.log(queryKey, filterParams, "eeeeeee")
        return { filterParams, setFilterParams }
    }
    console.log(queryKey, currentParams, "ssssss")
    return { filterParams: currentParams, setFilterParams }
}

export default useFilterParams
