import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query';

const useGetItems = (queryKey) => {

    const queryValues = useQuery({
        queryKey: [queryKey],
        enabled: false
    })

    return { items: queryValues.data?.items, pagination: queryValues.data?.pagination }
}

export default useGetItems
