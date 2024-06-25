import { AssetTable } from '../../../core/components/AssetTable';
import useGetItems from '../../../core/hooks/useGetItems';
import { defaultAssetColumns } from '../../utils/utils';
import { CHAMBER } from '../../queries';
import { AssetsDataType } from '../../../core/types/types';
import { get as _get } from 'lodash'

export const ChamberTable = () => {
    const { items, isFetching, refetch, pagination } = useGetItems(CHAMBER);

    //params = useParams from react-router

    const onPaginationChange = (a) => {
        console.log(a)
        // fetch current params from url
        // set new page values using the current params
        // useNavaigate with the new query params added to the url
        // the are page_size. page_num
    }

    return (
        <div>
            <AssetTable
                data={items as AssetsDataType[] || []}
                isLoading={isFetching}
                assetColumns={defaultAssetColumns}
                assetName={'CHAMBERS'}
                refetch={refetch}
                manualPagination={true}
                rowCount={_get(pagination, 'num_items')}
                pageCount={_get(pagination, 'num_pages')}
                pagination={
                { pageIndex: _get(pagination, 'current_page', 1) - 1,
                  pageSize: _get(pagination, 'page_size', 100)
                }}
                onPaginationChange={onPaginationChange}
            />
        </div>
    );
};
