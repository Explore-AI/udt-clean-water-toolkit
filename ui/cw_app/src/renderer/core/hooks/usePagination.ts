import { useState } from "react";
import { type MRT_PaginationState} from 'mantine-react-table'


const usePagination = () => {
    const [pagination, setPagination] = useState<MRT_PaginationState>({
        pageIndex: 0,
        pageSize: 20,
    });
    const { pageIndex, pageSize } = pagination;
    return { pagination, setPagination, pageIndex, pageSize }
}

export default usePagination; 