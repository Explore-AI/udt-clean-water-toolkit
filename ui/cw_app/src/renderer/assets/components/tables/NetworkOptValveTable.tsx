import { AssetTable } from "../../../core/components/AssetTable";
import useGetData from '../../../core/hooks/useGetData';
import { defaultAssetColumns } from '../../utils/utils';
import { NETWORK_OPT_VALVE } from '../../queries';
import { AssetsDataType } from '../../../core/types/types';
import { ApiResponse } from '../../types/types';

export const NetworkOptValveTable = () => {
    const { queryValues } = useGetData(NETWORK_OPT_VALVE);
    const { data, isFetching, refetch } = queryValues;
    const assetData = data as ApiResponse || [];

    return (
        <div>
            <AssetTable
                data={assetData.items as AssetsDataType[] || []}
                isLoading={isFetching}
                assetColumns={defaultAssetColumns}
                assetName={'NETWORK OPT VALVE'}
                refetch={refetch}
            />
        </div>
    );
};