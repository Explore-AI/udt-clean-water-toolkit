// Define the interface for each layer toggle
export interface LayerToggle {
    visible: boolean;
    label: string;
    key: string;
}

// Define the interface for the toggle object
export interface LayerToggleObject {
    chambers: LayerToggle;
    distribution_main: LayerToggle;
    hydrants: LayerToggle;
    loggers: LayerToggle;
    network_meter: LayerToggle;
    network_opt_valve: LayerToggle;
    operational_site: LayerToggle;
    pressure_control_valve: LayerToggle;
    pressure_fitting: LayerToggle;
    trunkmain: LayerToggle;
}

export interface BasemapToggle {
    visible: boolean;
    label: string;
    map_url?: string;
    key: string;
}

export interface BasemapToggleObject {
    open_street_map: BasemapToggle;
    satellite_map: BasemapToggle;
    dark_map: BasemapToggle;
    terrain: BasemapToggle;
}

export interface NominatimRequestProps {
    urlExtension: string; 
    params: {
        q: string; 
        format: string; 
        limit: number;
        addressdetails: number;
    }; 
}

interface NominatimAddressDetails {
    borough?: string; 
    'ISO3166-2-lvl4'?: string;
    'ISO3166-2-lvl6'?: string;
    city: string;
    country:string;
    country_code?: string;
    man_made?: string;
    postcode?: string;
    quarter?: string;
    road?: string;
    state?: string;
    state_district?: string;
}

export interface NominatimResponseData {
    address: NominatimAddressDetails; 
    addresstype: string; 
    boundingbox: string[];
    category: string; 
    display_name: string;
    importance: number; 
    lat: string; 
    licence: string; 
    lon: string; 
    name: string; 
    osm_id: number; 
    osm_type: string;
    place_id: number; 
    place_rank: number; 
    type: string;
}
