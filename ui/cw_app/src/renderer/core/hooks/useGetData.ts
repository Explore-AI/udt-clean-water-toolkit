import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query';

const useGetData = (queryKey) => {

    const queryValues = useQuery({
        queryKey: [queryKey]
    })

    return queryValues
}

export default useGetData
