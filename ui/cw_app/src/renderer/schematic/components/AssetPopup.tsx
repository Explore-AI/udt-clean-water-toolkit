// create a popup for the asset node's properties
import styles from '../css/AssetPopup.module.css';
import { AssetPopupProps } from '../types/types';
import { IconXboxX } from '@tabler/icons-react';
import { CloseButton } from '@mantine/core';
import { getIcons } from './IconComponents';

export const AssetPopup: React.FC<AssetPopupProps> = ({
    nodeProps,
    onClose,
}) => {

    const assetIcon = nodeProps?.label
                    ? getIcons(nodeProps?.label)
                    : getIcons('default');

    return (
        <>
            <div className={styles.popupContainer}>
                {/* <div className={styles.closeButton}>
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
                    </div> */}
                <div className={styles.title}>
                    <div className={styles.icon}>{assetIcon}</div>
                    <div>
                        <div><strong> {nodeProps.label} </strong></div>
                    </div>
                    <div style={{ textAlign: 'right', fontWeight: 300 }}>
                        <div>{null}</div>
                    </div>
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
                <hr />
                <div className={styles.details}>
                    { nodeProps?.tag &&
                      <div>
                          <strong>Tag: </strong>{' '}
                          {nodeProps.tag}
                      </div>
                    }
                    <div>
                        <strong>DMA Codes:</strong>{' '}
                        {nodeProps.code || "ZMAIDL45" }
                    </div>
                    <div>
                        <strong>DMA Names:</strong>{' '}
                        { nodeProps.name || "MAIDA VALE" }
                    </div>
                    <div>
                        <strong>Coordinates:</strong>{' '}
                        {` ${nodeProps.coords_27700[0]}, ${nodeProps.coords_27700[1]}`}
                    </div>
                    <div>
                        <strong>Node Types:</strong> {nodeProps.label}
                    </div>
                    <div>
                        <strong>Utility:</strong> {nodeProps.utility || "Thames Water"}
                    </div>
                </div>
            </div>
        </>
    );
};
