import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query'
import { get as _get, isEmpty as _isEmpty } from 'lodash'

const useSetFilterParams = (queryKey, params={}) => {

    const queryClient = useQueryClient()

    const allParams = queryClient.getQueryData('filterParams')
    const currentParams = _get(allParams, `${queryKey}`, {})

    let newParams
    if (!_isEmpty(params)) {
        newParams = { ...currentParams, ...params }
        queryClient.setQueryData('filterParams', { [queryKey]: newParams })
        return newParams
    }

    return currentParams
}

export default useSetFilterParams
