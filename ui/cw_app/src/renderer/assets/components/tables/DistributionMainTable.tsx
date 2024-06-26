import { BaseTable } from '../../../core/components/BaseTable';
import useGetItems from '../../../core/hooks/useGetItems';
import { defaultAssetColumns } from '../../utils/utils';
import { DIST_MAINS } from '../../queries';
import { AssetsDataType } from '../../../core/types/types';
import { get as _get } from 'lodash';
import { ApiResponse } from '../../types/types';
import usePagination from '../../../core/hooks/usePagination';
import useFetchItems from '../../../core/hooks/useFetchItems';

export const DistributionMainTable = () => {
    // const { items, isFetching, refetch, pagination } = useGetItems(DIST_MAINS);
    const { pagination: localPagination, setPagination } = usePagination();

    const { queryValues } = useFetchItems(DIST_MAINS, {
        params: {
            page: localPagination.pageIndex + 1,
            page_size: localPagination.pageSize,
        },
    });
    const { data, isFetching, refetch} = queryValues; 
    const { items, pagination } = data || {};

    return (
        <div>
            <BaseTable
                data={items as AssetsDataType[] || []}
                isLoading={isFetching}
                assetColumns={defaultAssetColumns}
                assetName={'DISTRIBUTION MAINS'}
                refetch={refetch}
                manualPagination={true}
                rowCount={_get(pagination, 'num_items')}
                pageCount={_get(pagination, 'num_pages')}
                pagination={localPagination}
                onPaginationChange={setPagination}
            />
        </div>
    );
};