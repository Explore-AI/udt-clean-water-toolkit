// create a popup for the asset node's properties
import styles from '../css/AssetPopup.module.css';
import { AssetPopupProps } from '../types/types';
import { IconXboxX } from '@tabler/icons-react';
import { CloseButton } from '@mantine/core';

export const AssetPopup: React.FC<AssetPopupProps> = ({
    nodeProps,
    onClose,
}) => {
    console.log(nodeProps)
    return (
        <>
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
                    {/* <div className={styles.icon}>{icon}</div> */}
                    <div>
                        <div><strong> {nodeProps.label} </strong></div>
                    </div>
                    <div style={{ textAlign: 'right', fontWeight: 300 }}>
                        <div>{null}</div>
                    </div>
                </div>
                <hr />
                <div className={styles.details}>
                    <div>
                        <strong>DMA Codes:</strong>{' '}
                        {nodeProps.code || 'ZCHIPO01'}
                    </div>
                    <div>
                        <strong>DMA Names:</strong>{' '}
                        {nodeProps.name || 'OVER NORTON'}
                    </div>
                    <div>
                        <strong>Coordinates:</strong>{' '}
                        {` ${nodeProps.coords_27700[0]}, ${nodeProps.coords_27700[1]}`}
                    </div>
                    <div>
                        <strong>Node Types:</strong> Pipe Junction
                    </div>
                    <div>
                        <strong>Utility:</strong> Thames Water
                    </div>
                </div>
            </div>
        </>
    );
};
