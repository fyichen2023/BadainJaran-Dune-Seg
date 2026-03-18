# Badain Jaran Megadune Atlas  
*Physics-Informed Differentiable Cellular Automata for Instance Segmentation and 3D Morphodynamics*  

![Data Available](https://img.shields.io/badge/Data-Available-success)  
![Framework](https://img.shields.io/badge/Framework-PyTorch-red)  
![Status](https://img.shields.io/badge/Status-Pre--release-orange)  
![License](https://img.shields.io/badge/License-See%20Repository-blue)

---

## 1) Overview

### English
This project focuses on high-precision instance segmentation and 3D morphometric parameter extraction of complex megadunes in the **Badain Jaran Desert**.  
We propose a novel end-to-end deep learning framework that integrates **aeolian dynamics priors** (e.g., prevailing wind direction, lee-slope behavior, and angle-of-repose constraints) with a **Physics-Informed Differentiable Cellular Automata (Differentiable CA)** architecture.  

The current release provides desert-wide dune instance products and derived geometric/dynamic attributes for academic evaluation and project demonstration.  
These datasets are intended to support future manuscript preparation and submission after iterative refinement.

### 中文
本项目面向**巴丹吉林沙漠**复杂高大沙山（Megadunes）的高精度实例分割与三维形态参数提取。  
我们提出了一种新型端到端深度学习框架，将**风沙动力学先验**（如主风向、背风坡演化规律、休止角约束）与**物理约束可微分元胞自动机**相结合。  

当前版本发布了全沙漠尺度的沙山实例分割成果及其几何—动力学属性参数，用于学术评估与阶段性项目展示。  
相关成果将于后续持续完善，并用于未来论文撰写与投稿准备。

---

## 2) ⚠️ Status & Disclaimer

> [!WARNING]  
> **English**  
> The original Physics-Informed Differentiable Cellular Automata network architecture is currently in the **pre-release stage**.  
> To protect core intellectual property, the **full PyTorch training code** and **pretrained weights** are **not publicly available at this stage**.  
> At present, the repository Releases page provides the **first public V1.0 data release** of dune instance segmentation and morphometric attributes for academic assessment and project reporting.  
> The complete codebase will be open-sourced in a later stage.
>
> **中文**  
> 本项目底层原创“物理约束可微分元胞自动机”网络架构目前处于**预发布阶段**。  
> 为保护核心知识产权，**完整 PyTorch 训练源码**与**预训练权重**暂不公开。  
> 当前仓库 Releases 页面仅首发 **V1.0 沙丘实例分割与形态学属性数据**，供学术评估与阶段性项目结项展示使用。  
> 完整代码将在后续阶段逐步开源。

---

## 3) Data Access & Downloads

### English
All released datasets are packaged and distributed via the repository **Releases** page, including:

- **Raster data**:  
  - `dune_instance_label.tif`
- **Spatial vector databases**:  
  - `dune_database.shp`  
  - `dune_database.gpkg`
- **Attribute tables**:  
  - `dune_attributes.csv`  
  - `dune_attributes.xlsx`

Please navigate to the **Releases** section of this repository to download the latest versioned data package (currently V1.0 pre-release).

### 中文
所有已发布数据均已打包并上传至本仓库 **Releases** 页面，包括：

- **栅格数据**：  
  - `dune_instance_label.tif`
- **空间矢量数据库**：  
  - `dune_database.shp`  
  - `dune_database.gpkg`
- **属性数据表**：  
  - `dune_attributes.csv`  
  - `dune_attributes.xlsx`

请前往仓库 **Releases** 页面下载最新版本化数据包（当前为 V1.0 预发布数据）。

---

## 4) Data Dictionary (Bilingual)

| Field | English Description | 中文说明 |
|---|---|---|
| `Dune_ID` | Unique identifier of each dune instance | 沙山唯一标识号 |
| `Partition` | Administrative/analytical partition or subregion label | 所属区划/分区 |
| `Center_X` | X coordinate of dune centroid (longitude or projected X) | 地理中心 X 坐标（经度/投影坐标） |
| `Center_Y` | Y coordinate of dune centroid (latitude or projected Y) | 地理中心 Y 坐标（纬度/投影坐标） |
| `Density_km2` | Spatial density of dunes (count per km²) | 空间分布密度（个/平方公里） |
| `RelHeight` | Relative dune height (m) | 相对高度（米） |
| `Volume` | Dune volume (m³) | 沙山体积（立方米） |
| `Slope_Mean` | Mean slope angle (degrees) | 平均坡度（度） |
| `Slope_Max` | Maximum slope angle (degrees) | 最大坡度（度） |
| `ReposeArea` | Surface area within angle-of-repose range (28°–38°), in m² | 处于休止角状态（28°–38°）的表面积（平方米） |
| `Repose_Pct` | Proportion of repose-angle area (%) | 休止角面积占比（%） |
| `Curvature` | Mean surface curvature | 表面平均曲率 |
| `Strike_Deg` | Orientation of primary ridge/major axis (degrees) | 主脊线/长轴走向（度） |
| `Aspect_Rat` | Aspect ratio (width-to-height ratio) | 宽高比 |

---

## 5) Contact

- **Project Maintainer / 项目维护者**: `@fyichen2023`  
- **Repository / 项目地址**: https://github.com/fyichen2023/BadainJaran-Dune-Seg
