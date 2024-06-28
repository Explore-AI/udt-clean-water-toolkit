import { BaseTable } from '../../../core/components/BaseTable';
import { defaultAssetColumns } from '../../utils/utils';
import { TRUNK_MAINS } from '../../queries';
import { AssetsDataType } from '../../../core/types/types';
import { get as _get } from 'lodash';
import usePagination from '../../../core/hooks/usePagination';
import useFetchItems from '../../../core/hooks/useFetchItems';
import useGetItems from '../../../core/hooks/useGetItems';

export const TrunkMainTable = () => {
    // const { items, isFetching, refetch, pagination } = useGetItems(TRUNK_MAINS);
    const { pagination: localPagination, setPagination } = usePagination();
    const { queryValues } = useFetchItems(TRUNK_MAINS, {
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
                data={(items as AssetsDataType[]) || []}
                isLoading={isFetching}
                assetColumns={defaultAssetColumns}
                assetName={'TRUNK MAINS'}
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
