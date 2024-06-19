// create a popup for the asset node's properties
import { AssetPopupProps } from '../types/types';
import styles from '../css/AssetPopup.module.css';
import { getIcons } from './IconComponents';
import { getDmas } from '../utils/schematicUtils';
import { IconXboxX } from '@tabler/icons-react';
import { CloseButton } from '@mantine/core';
import Draggable from 'react-draggable';

export const AssetPopup: React.FC<AssetPopupProps> = ({
    nodeProps,
    onClose,
}) => {
    const { data } = nodeProps;
    const assetName = data.properties?.asset_names
        ? data.properties.asset_names[0]
        : 'Point Asset';
    const icon = getIcons(assetName);
    const assetId = data.properties?.asset_gids
        ? data.properties.asset_gids[0]
        : data.id;
    const { x, y } = data.position;
    const assetCoords = [x.toPrecision(5), y.toPrecision(5)];
    const assetDmas = getDmas(data.properties?.dmas || '');
    const assetTypes = data.properties?.node_types
        ? data.properties?.node_types
        : ['NA'];
    const assetUtility = data.properties?.utility
        ? data.properties.utility
        : 'NA';

    return (
        <>
            <Draggable>
                <div className={styles.popupContainer}>
                    <div className={styles.closeButton}>
                        <CloseButton
                            onClick={onClose}
                            icon={
                                <IconXboxX
                                    size={16}
                                    stroke={2}
                                    color="#EB9486"
                                />
                            }
                        />
                    </div>
                    <div className={styles.title}>
                        <div className={styles.icon}>{icon}</div>
                        <div>
                            <div><strong> {data.properties?.label} </strong></div>
                        </div>
                        <div style={{ textAlign: 'right', fontWeight: 300 }}>
                            <div>{assetId}</div>
                        </div>
                    </div>
                    <hr />
                    <div className={styles.details}>
                        <div>
                            <strong>DMA Codes:</strong>{' '}
                            {assetDmas.codes.join(', ')}
                        </div>
                        <div>
                            <strong>DMA Names:</strong>{' '}
                            {assetDmas.names.join(', ')}
                        </div>
                        <div>
                            <strong>Asset Coordinates:</strong>{' '}
                            {` ${assetCoords[0]}, ${assetCoords[1]}`}
                        </div>
                        <div>
                            <strong>Node Types:</strong> {assetTypes.join(', ')}
                        </div>
                        <div>
                            <strong>Utility:</strong> {assetUtility}
                        </div>
                    </div>
                </div>
            </Draggable>
        </>
    );
};
