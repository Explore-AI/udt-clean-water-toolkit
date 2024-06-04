import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query'
import { get as _get, isEmpty as _isEmpty } from 'lodash'

const useGetFilterParams = (queryKey) => {

    const queryClient = useQueryClient()

    const allParams = queryClient.getQueryData('filterParams')
    const params = _get(allParams, `${queryKey}`, {})

    return params
}

export default useGetFilterParams
