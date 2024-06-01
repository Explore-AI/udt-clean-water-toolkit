import { DRF_API_URL } from '../../config';
import { isEmpty as _isEmpty, keys as _keys, reduce as _reduce, } from "lodash";

export const getBaseUrl = (querykey, params) => {
    console.log("yyyy")
    console.log("qqqqq", queryKey)

    if (!_isEmpty(params)) {
        return `${DRF_API_URL}/${queryKey}/${params}`
    } else {
        return `${DRF_API_URL}/${queryKey}/`
    }
}

export const serialize = (params) => {
    return (
        "?" +
        _reduce(
            _keys(params),
            (encodedParams, key) => {
                if (params[key] !== null && params[key] !== undefined) {
                    encodedParams.push(key + "=" + encodeURIComponent(params[key]));
                }
                return encodedParams;
            },
            []
        ).join("&")
    );
}
