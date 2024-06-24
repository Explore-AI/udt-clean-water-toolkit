import { AssetTable } from '../../../core/components/AssetTable';
import useGetData from '../../../core/hooks/useGetData';
import { defaultAssetColumns } from '../../utils/utils';
import { PRESSURE_FITTING } from '../../queries';
import { AssetsDataType } from '../../../core/types/types';
import { ApiResponse } from '../../types/types';

export const PressureFittingTable = () => {
    const { queryValues } = useGetData(PRESSURE_FITTING);
    const { data, isFetching, refetch } = queryValues;
    const assetData = data as ApiResponse || [];

    return (
        <div>
            <AssetTable
                data={assetData.items as AssetsDataType[] || []}
                isLoading={isFetching}
                assetColumns={defaultAssetColumns}
                assetName={'PRESSURE FITTING'}
                refetch={refetch}
            />
        </div>
    );
};