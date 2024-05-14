import * as styles from '../css/TogglePopup.module.css'; 

interface ToggleProps {
    message: string;
}

export default function ToggleViewPopup({message}: ToggleProps) {
    return(
        <>
            <div className={styles.container}> 
                <p> Here is a toggle popup window </p>
                <p>{message}</p>
            </div>
        </>
    )
}