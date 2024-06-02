import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query';

const useGetData = (queryKey) => {

    const queryValues = useQuery({
        queryKey: [queryKey],
        enabled: false
    })

    return queryValues
}

export default useGetData
