import { useRef, useEffect } from 'react'
import { isEqual } from 'lodash'

function usePrevious(value) {
    const ref = useRef()

    useEffect(() => {
        if (!isEqual(ref.current, value)) {
            ref.current = value;
        }
    },[value])
    return ref.current
}

export default usePrevious
