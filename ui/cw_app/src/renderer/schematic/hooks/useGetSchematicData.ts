import { useQuery } from '@tanstack/react-query';

const useGetSchematicData = (queryKey: string[]) => {
    const queryValues =  useQuery({
        queryKey: queryKey,
        enabled: false,
    });
    return queryValues; 
};

export default useGetSchematicData;
