import { AssetTable } from '../../../core/components/AssetTable';
import useGetData from '../../../core/hooks/useGetData';
import { defaultAssetColumns } from '../../utils/utils';
import { NETWORK_METER } from '../../queries';
import { AssetsDataType } from '../../../core/types/types';
import { ApiResponse } from '../../types/types';

export const NetworkMeterTable = () => {
    const { queryValues } = useGetData(NETWORK_METER);
    const { data, isFetching, refetch } = queryValues;
    const assetData = data as ApiResponse || [];

    return (
        <div>
            <AssetTable
                data={assetData.items as AssetsDataType[] || []}
                isLoading={isFetching}
                assetColumns={defaultAssetColumns}
                assetName={'NETWORK METERS'}
                refetch={refetch}
            />
        </div>
    );
};