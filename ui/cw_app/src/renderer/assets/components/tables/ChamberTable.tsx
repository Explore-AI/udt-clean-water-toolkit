import { AssetTable } from '../../../core/components/AssetTable';
import useGetData from '../../../core/hooks/useGetData';
import { defaultAssetColumns } from '../../utils/utils';
import { CHAMBER } from '../../queries';
import { AssetsDataType } from '../../../core/types/types';
import { ApiResponse } from '../../types/types';

export const ChamberTable = () => {
    const { queryValues } = useGetData(CHAMBER);
    const { data, isFetching, refetch } = queryValues;
    const assetData = data as ApiResponse || [];

    return (
        <div>
            <AssetTable
                data={assetData.items as AssetsDataType[] || []}
                isLoading={isFetching}
                assetColumns={defaultAssetColumns}
                assetName={'CHAMBERS'}
                refetch={refetch}
            />
        </div>
    );
};