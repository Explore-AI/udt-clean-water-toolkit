import geopandas as gpd
import fiona
import timeit

def report_generator(layer_path):
    print("Auditing DB")
    f = open("/Users/chelsea/Documents/db_audit.txt", "w")
    f.write(f'Report for DB {layer_path} /n')
    layers = fiona.listlayers(layer_path)
    layers_filtered = [l for l in layers if not l.endswith('Anno') and l.startswith('w')]
    for l in layers_filtered:
        start = timeit.timeit()
        print(f"Auditing layer {l}")
        layer_gdf = gpd.read_file(layer_path, layer=l)
        print(f"read layer {l}")
        layer_info = {}
        geoms = set(layer_gdf.geom_type)
        proj = layer_gdf.crs.to_epsg()
        is_geom_net = True if 'ENABLED' in layer_gdf.columns else False
        f.write(f"""
            Layer Name: {l}
            Geometry Types: {geoms}
            Projection: {proj}
            Part of Network: {is_geom_net} /n
              """)
        print(f"""
            Layer Name: {l}
            Geometry Types: {geoms}
            Projection: {proj}
            Part of Network: {is_geom_net} /n
              """)
        layer_info[l] = [geoms, proj, is_geom_net]
        col_info = {}
        print("Column_name  Null_Percentage  Column_Type /n")
        for col in layer_gdf.columns:
            try:
                col_info[col] = [layer_gdf[col].isnull().sum() * 100 / len(layer_gdf), layer_gdf[col].dtype]
                f.write(f"{col}  {str(round(col_info[col][0], 2))}  {col_info[col][1]} /n")
            except Exception as ex: 
                reason = f"couldnt process column {col}, reason {ex}"
        layer_info[l].append(col_info)  
        end = timeit.timeit()
        time_for_layer = end - start
        f.write(f"Audited layer {l}, took {time_for_layer}")
    f.close() 
    print("DB Audited")

        
if __name__ == "__main__":
    report_generator("/Users/chelsea/Documents/CW_20231108_060001.gdb")


