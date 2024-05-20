// add our utility functions here
import { gpsRegex } from '..';
import axios from 'axios';
import { NOMINATIM_URL } from '../../config';
import {
    NominatimRequestProps,
} from '../../map/types/types';

export const getNominatimData = async (
    props: NominatimRequestProps,
): Promise<{ lat: number; lon: number }> => {
    const params = { ...props.params };
    return axios
        .get(NOMINATIM_URL + props.urlExtension, { params })
        .then((response) => {
            const updatedLatLong = {
                lat: parseFloat(response.data[0].lat),
                lon: parseFloat(response.data[0].lon),
            };
            return updatedLatLong;
        });
};

export const getCoordinateData = () => {};

export const getAddressData = ({}) => {};

export const getAssetData = () => {
    // after receiving the asset id, whether it be gisid, dma, or fmz then make a request to the
    // geoserver api to collect the data
};

export const validateInput = (inputString: string) => {
    const searchString = inputString.trim();
    if (searchString == '') return { validated: false, type: '', payload: '' };
    // gps input type
    if (gpsRegex.test(searchString)) {
        const formattedString = searchString.replace(' ', '');
        // get the coordinates of the gps
        const coords = formattedString.split(',');
        return {
            validated: true,
            type: 'gps',
            payload: [parseFloat(coords[0]), parseFloat(coords[1])],
        };
    }
    return { validated: true, type: 'generic', payload: searchString };
};


export const isValidCoordinate = (lat: number, lon: number) => {
    return lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180;
  };