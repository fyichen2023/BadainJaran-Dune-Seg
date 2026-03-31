import os
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.features import shapes
from shapely.geometry import shape
import geopandas as gpd
import pandas as pd
from rasterio.transform import rowcol
from scipy.spatial import KDTree
from tqdm import tqdm
import warnings
import gc

warnings.filterwarnings('ignore')


def _env_path(name, default_path):
    value = os.getenv(name)
    return value if value else default_path

def main():
    print("====================================")
    print("沙山形态参数数据库自动提取工具 (内存优化版)")
    print("====================================")

    # ==========================
    # 路径配置
    # ==========================
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(project_root, "data")
    raster_dir = os.path.join(data_dir, "rasters")
    vector_dir = os.path.join(data_dir, "vectors")

    mask_path = _env_path("DUNE_MASK_PATH", os.path.join(raster_dir, "mask.tif"))
    dem_path = _env_path("DUNE_DEM_PATH", os.path.join(raster_dir, "dem.tif"))
    slope_path = _env_path("DUNE_SLOPE_PATH", os.path.join(raster_dir, "slope.tif"))
    aspect_path = _env_path("DUNE_ASPECT_PATH", os.path.join(raster_dir, "aspect.tif"))
    area_path = _env_path("DUNE_AREA_PATH", os.path.join(vector_dir, "area.shp"))

    output_dir = _env_path("DUNE_OUTPUT_DIR", os.path.join(project_root, "output", "dune_database"))
    os.makedirs(output_dir, exist_ok=True)
    
    output_shp = os.path.join(output_dir, "dune_database.shp")
    output_csv = os.path.join(output_dir, "dune_attributes.csv")
    output_gpkg = os.path.join(output_dir, "dune_database.gpkg")
    output_xlsx = os.path.join(output_dir, "dune_attributes.xlsx")

    # ==========================
    # 1. 读取基础掩膜并获取元数据
    # ==========================
    print("正在加载 Mask 数据...")
    with rasterio.open(mask_path) as src_mask:
        mask_data = src_mask.read(1)
        transform = src_mask.transform
        crs = src_mask.crs
        res_x = abs(src_mask.res[0])
        res_y = abs(src_mask.res[1])
        height = src_mask.height
        width = src_mask.width
        pixel_area = res_x * res_y

    print(f"数据分辨率: {res_x}m x {res_y}m")
    
    # 获取各个数据的 no_data 值
    with rasterio.open(dem_path) as src_dem: dem_nodata = src_dem.nodata
    with rasterio.open(slope_path) as src_slope: slope_nodata = src_slope.nodata
    with rasterio.open(aspect_path) as src_aspect: aspect_nodata = src_aspect.nodata

    # ==========================
    # 2. 矢量化单体掩膜
    # ==========================
    print("正在执行掩膜矢量化与边界自动提取...")
    valid_mask = (mask_data > 0)
    shapes_list = list(shapes(mask_data, mask=valid_mask, transform=transform))

    polygons = []
    instance_ids = []
    for geom, val in tqdm(shapes_list, desc="矢量化单体多边形", bar_format="{l_bar}{bar:30}{r_bar}"):
        poly = shape(geom).buffer(0)
        polygons.append(poly)
        instance_ids.append(int(val))

    df = pd.DataFrame({'Dune_ID': instance_ids, 'geometry': polygons})
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=crs)
    gdf = gdf.dissolve(by='Dune_ID').reset_index()

    # ==========================
    # 3. 空间相交：获取所属分区
    # ==========================
    partition_col = 'Partition'
    gdf[partition_col] = 'Unknown'
    if os.path.exists(area_path):
        print("正在获取所属分区属性...")
        try:
            area_gdf = gpd.read_file(area_path)
            if area_gdf.crs != crs:
                area_gdf = area_gdf.to_crs(crs)
            joined = gpd.sjoin(gdf, area_gdf, how='left', predicate='intersects')
            
            possible_cols = [c for c in area_gdf.columns if c != 'geometry']
            if len(possible_cols) > 0:
                target_col = possible_cols[0]
                joined = joined[~joined.index.duplicated(keep='first')]
                gdf[partition_col] = joined[target_col].fillna('Unknown')
            else:
                gdf[partition_col] = 'Study Area'
        except Exception as e:
            print(f"叠加分区文件失败: {e}")
    else:
        print("未找到分区 Shapefile (area.shp)，跳过所属分区标注。")

    # ==========================
    # 4. 基于 Window 的内存高效切片提参
    # ==========================
    print("正在计算形态属性参数与空间分布特征...")

    metrics = []

    with rasterio.open(dem_path) as src_dem, \
         rasterio.open(slope_path) as src_slope, \
         rasterio.open(aspect_path) as src_aspect:

        for idx, row in tqdm(gdf.iterrows(), total=len(gdf), desc="逐单体形态属性提取", bar_format="{l_bar}{bar:30}{r_bar}"):
            inst_id = row['Dune_ID']
            geom = row['geometry']
            
            # 使用多边形 bounding box 构建窗口
            minx, miny, maxx, maxy = geom.bounds
            row1, col1 = rowcol(transform, minx, maxy)
            row2, col2 = rowcol(transform, maxx, miny)
            
            # 使用缓冲，确保能盖住所有的掩膜像元
            min_row = max(0, min(row1, row2) - 1)
            max_row = min(height, max(row1, row2) + 1)
            min_col = max(0, min(col1, col2) - 1)
            max_col = min(width, max(col1, col2) + 1)
            
            if max_row <= min_row or max_col <= min_col:
                continue
            
            pad_min_row = max(0, min_row - 1)
            pad_min_col = max(0, min_col - 1)
            pad_max_row = min(height, max_row + 1)
            pad_max_col = min(width, max_col + 1)
            
            win_padded = Window.from_slices((pad_min_row, pad_max_row), (pad_min_col, pad_max_col))
            
            # 以 padded 窗口读取数据
            dem_chunk = src_dem.read(1, window=win_padded).astype(np.float32)
            slope_chunk = src_slope.read(1, window=win_padded).astype(np.float32)
            aspect_chunk = src_aspect.read(1, window=win_padded).astype(np.float32)
            
            # NoData 替换
            if dem_nodata is not None: dem_chunk[dem_chunk == dem_nodata] = np.nan
            if slope_nodata is not None: slope_chunk[slope_chunk == slope_nodata] = np.nan
            if aspect_nodata is not None: aspect_chunk[aspect_chunk == aspect_nodata] = np.nan
            
            # 安全防爆内存：如果该单体由于拓扑错误或确实极大，导致生成数十GB的浮点矩阵，这部分内存需要极度节约
            box_area = (pad_max_row - pad_min_row) * (pad_max_col - pad_min_col)
            if box_area > 40000000: # 如果边框超过例如 6000*6000，可能直接忽略曲率计算以自保
                curv_chunk = np.full(dem_chunk.shape, np.nan, dtype=np.float32)
            else:
                # 局部计算曲率 (使用 padded 数据) 并强制声明为 float32 (防默认 float64 暴增一倍内存)
                dzdy, dzdx = np.gradient(dem_chunk)
                dzdy = dzdy.astype(np.float32) / res_y
                dzdx = dzdx.astype(np.float32) / res_x
                d2zdy2, _ = np.gradient(dzdy)
                _, d2zdx2 = np.gradient(dzdx)
                
                curv_chunk = (d2zdx2.astype(np.float32) / res_x) + (d2zdy2.astype(np.float32) / res_y)
                
                # 必须彻底释放中间矩阵
                del dzdy, dzdx, d2zdy2, d2zdx2
            
            # 扣除 padding 后提取出正好覆盖 Box 的区域
            row_offset = min_row - pad_min_row
            col_offset = min_col - pad_min_col
            h_box = max_row - min_row
            w_box = max_col - min_col
            
            dem_slice = dem_chunk[row_offset:row_offset+h_box, col_offset:col_offset+w_box]
            slope_slice = slope_chunk[row_offset:row_offset+h_box, col_offset:col_offset+w_box]
            aspect_slice = aspect_chunk[row_offset:row_offset+h_box, col_offset:col_offset+w_box]
            curv_slice = curv_chunk[row_offset:row_offset+h_box, col_offset:col_offset+w_box]
            
            # 拿到 Box 中的精确实例掩膜
            inst_mask = (mask_data[min_row:max_row, min_col:max_col] == inst_id)
            
            dem_valid = dem_slice[inst_mask]
            slope_valid = slope_slice[inst_mask]
            aspect_valid = aspect_slice[inst_mask]
            curv_valid = curv_slice[inst_mask]
            
            # ================= 计算指标 =================
            center_x = geom.centroid.x
            center_y = geom.centroid.y
            
            dem_valid_nonan = dem_valid[~np.isnan(dem_valid)]
            if len(dem_valid_nonan) > 0:
                dem_min = np.nanmin(dem_valid_nonan)
                dem_max = np.nanmax(dem_valid_nonan)
                rel_height = dem_max - dem_min
                volume = np.sum(dem_valid_nonan - dem_min) * pixel_area
            else:
                rel_height = np.nan
                volume = np.nan
            
            slope_valid_nonan = slope_valid[~np.isnan(slope_valid)]
            slope_mean = np.nanmean(slope_valid_nonan) if len(slope_valid_nonan) > 0 else np.nan
            slope_max = np.nanmax(slope_valid_nonan) if len(slope_valid_nonan) > 0 else np.nan
            
            # 休止角区域 (东南向 90°-180°, 坡高一般 >30°)
            valid_repose = ~np.isnan(aspect_valid) & ~np.isnan(slope_valid)
            aspect_for_repose = aspect_valid[valid_repose]
            slope_for_repose = slope_valid[valid_repose]
            
            # 当 Aspect 提供格式为度数时：
            repose_mask = (aspect_for_repose >= 90) & (aspect_for_repose <= 180) & (slope_for_repose >= 30)
            repose_area = np.sum(repose_mask) * pixel_area
            repose_pct = (repose_area / (np.sum(inst_mask) * pixel_area)) * 100
            
            curv_mean = np.nanmean(curv_valid[~np.isnan(curv_valid)]) if len(curv_valid) > 0 else np.nan
            
            # 最小外接矩形测算（长轴走向、长宽比）
            mrr = geom.minimum_rotated_rectangle
            if mrr.geom_type == 'Polygon':
                coords = list(mrr.exterior.coords)
                dx1, dy1 = coords[1][0] - coords[0][0], coords[1][1] - coords[0][1]
                dx2, dy2 = coords[2][0] - coords[1][0], coords[2][1] - coords[1][1]
                
                len1 = np.hypot(dx1, dy1)
                len2 = np.hypot(dx2, dy2)
                
                if len1 > len2:
                    major_len, minor_len = len1, len2
                    dx, dy = dx1, dy1
                else:
                    major_len, minor_len = len2, len1
                    dx, dy = dx2, dy2
                    
                strike_deg = np.degrees(np.arctan2(dx, dy)) % 180
                aspect_ratio = (major_len / minor_len) if minor_len > 0 else np.nan
            else:
                strike_deg = np.nan
                aspect_ratio = np.nan

            metrics.append({
                'Dune_ID': inst_id,
                'Center_X': center_x,
                'Center_Y': center_y,
                'RelHeight': rel_height,
                'Volume': volume,
                'Slope_Mean': slope_mean,
                'Slope_Max': slope_max,
                'ReposeArea': repose_area, 
                'Repose_Pct': repose_pct,  
                'Curvature': curv_mean,    
                'Strike_Deg': strike_deg,  
                'Aspect_Rat': aspect_ratio 
            })
            
            # 清理本轮循环残存的大数组引用
            del dem_chunk, slope_chunk, aspect_chunk, curv_chunk
            del dem_slice, slope_slice, aspect_slice, curv_slice
            del dem_valid, slope_valid, aspect_valid, curv_valid, inst_mask
            
            if idx % 100 == 0:
                gc.collect()

    metrics_df = pd.DataFrame(metrics)
    gdf = gdf.merge(metrics_df, on='Dune_ID', how='inner')

    # ==========================
    # 5. 计算空间分布密度
    # ==========================
    print("正在计算空间分布密度特征 (Points per km^2 内)...")
    coords = np.vstack((gdf['Center_X'], gdf['Center_Y'])).T
    tree = KDTree(coords)
    search_radius = 5000 
    counts = tree.query_ball_point(coords, r=search_radius)
    area_km2 = np.pi * ((search_radius / 1000.0) ** 2)
    density = [(len(c) - 1) / area_km2 for c in counts]
    gdf['Density_km2'] = density

    # ==========================
    # 6. 数据交付与导出
    # ==========================
    print("正在保存输出结果...")
    
    for col in gdf.columns:
        if gdf[col].dtype == 'object':
            gdf[col] = gdf[col].fillna('')

    try:
        gdf.to_file(output_shp, encoding='utf-8')
        gdf.to_file(output_gpkg, driver="GPKG", encoding='utf-8')
    except Exception as e:
         print(f"空间数据保存遇到问题: {e}")
         
    df_out = pd.DataFrame(gdf.drop(columns=['geometry']))
    df_out.to_csv(output_csv, index=False, encoding='utf-8_sig')
    
    try:
        df_out.to_excel(output_xlsx, index=False)
    except ModuleNotFoundError:
        print("未检测到 openpyxl 包，已跳过 Excel 格式输出。请查收 CSV 文件。")

    print("\n✅ 处理全部完成！")
    print(f"数据总数: {len(gdf)} 个闭合多边形单体边界。")
    print(f"交付成果已保存至目录: {output_dir}")

if __name__ == "__main__":
    main()
