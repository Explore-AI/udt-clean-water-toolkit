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
