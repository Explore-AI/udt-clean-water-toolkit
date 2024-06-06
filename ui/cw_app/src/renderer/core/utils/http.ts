import { DRF_API_URL } from '../../config';
import { isEmpty as _isEmpty, keys as _keys, reduce as _reduce, } from "lodash";

export const getApiUrl = (queryKey, params={}) => {

    if (!_isEmpty(params)) {
        const queryParams = serialize(params)
        return `${DRF_API_URL}/${queryKey}/${queryParams}`
    } else {
        return `${DRF_API_URL}/${queryKey}/`
    }
}

export const queryFetch = async ({ signal }) =>  {
    const res = await fetch(url, { signal }) //TODO: replace with axios
    return await res.json();
}

const serialize = (params) => {
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
