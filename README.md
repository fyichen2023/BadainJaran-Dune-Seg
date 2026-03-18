# BadainJaran-MegaDune-Seg: Physics-Informed Instance Segmentation & 3-D Morphometry of Desert Megadunes

**巴丹吉林沙漠高大沙山物理先验增强实例分割与三维形态学参数提取**

[![Data Available](https://img.shields.io/badge/Data-Available%20on%20Releases-brightgreen?style=flat-square)](../../releases)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat-square&logo=pytorch)](https://pytorch.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)
[![Status: Pre-release](https://img.shields.io/badge/Status-Data%20Pre--release-orange?style=flat-square)]()
[![Under Review](https://img.shields.io/badge/Paper-Under%20Review-blue?style=flat-square)]()

---

## Overview

The **Badain Jaran Desert** (巴丹吉林沙漠) in Inner Mongolia, China, hosts some of the tallest stationary megadunes on Earth — rising up to 460 m above the surrounding interdune basins. Despite their remarkable scale, the three-dimensional (3-D) morphology and spatial dynamics of these megadunes remain poorly quantified at the desert-wide scale.

This repository presents **BadainJaran-MegaDune-Seg**, an end-to-end deep-learning framework for:

- **High-accuracy instance segmentation** of individual megadunes from multi-source remote sensing imagery (optical + DEM).
- **Desert-wide 3-D morphometric extraction**, including volume, relative height, slope statistics, surface curvature, crest orientation, and the extent of surfaces near the **angle of repose** (28 °–38 °).
- **Aeolian dynamics priors** — prevailing wind direction, lee-slope geometry, and repose-angle constraints — are encoded into a novel **Physics-Informed Differentiable Cellular Automaton (PIDCA)** backbone to improve segmentation accuracy and physical consistency.

The resulting geodatabase covers **the entire Badain Jaran Desert** and comprises vector polygons, raster derivatives, and a richly attributed morphometric table for every delineated megadune.

---

**巴丹吉林沙漠**位于中国内蒙古，是地球上发育最为壮观的复杂高大沙山区之一，单体沙山相对高差可达 460 米以上。然而，在全沙漠尺度上，对这些高大沙山三维形态与空间动力学的定量研究仍十分匮乏。

本仓库提供 **BadainJaran-MegaDune-Seg** 项目的公开数据资产。该项目构建了一套端到端深度学习框架，融合光学影像与高程数据，实现对全沙漠范围内高大沙山的高精度**实例分割**与**三维形态参数提取**（体积、相对高度、坡度统计、表面曲率、主脊走向及休止角面积比等）。其核心创新在于将风沙动力学先验（主风向、背风坡几何、休止角约束）嵌入一种新型**可微分元胞自动机（Differentiable Cellular Automaton, DCA）**骨干网络，兼顾分割精度与物理一致性。

---

## ⚠️ Status & Disclaimer — 重要状态声明与免责声明

> [!WARNING]
> **Code availability (English)**
>
> The core novelty of this project — the **Physics-Informed Differentiable Cellular Automaton (PIDCA)** network architecture — is currently **under review at an SCI-indexed peer-reviewed journal** (Pre-release / Under Review stage).
>
> To protect the intellectual property of the ongoing submission, **the complete PyTorch training source code and pre-trained model weights are temporarily withheld from public release**.
>
> The **Releases** page of this repository currently publishes **V1.0** of the megadune instance-segmentation and morphometric attribute dataset only — intended for academic evaluation and project reporting. Full code will be made openly available upon acceptance of the corresponding manuscript.

> [!WARNING]
> **代码可用性声明（中文）**
>
> 本项目的核心创新——**物理先验可微分元胞自动机（PIDCA）**网络架构——目前正处于 **SCI 顶刊同行评审阶段**（预发布 / 审稿中）。
>
> 为保护正在投稿的核心知识产权，**完整的 PyTorch 训练源码与预训练模型权重暂时不对外公开**。
>
> 本仓库 **Releases 页面**目前仅首发 **V1.0** 版本的沙丘实例分割结果与形态学属性数据，供学术评估与结项展示使用。完整代码将在对应论文正式被期刊接收后全面开源，敬请关注。

---

## 📦 Data Access & Downloads — 数据获取指南

All published data assets are packaged and hosted on the **[Releases](../../releases)** page of this repository.

| File | Format | Description |
|------|--------|-------------|
| `dune_database.gpkg` | GeoPackage (vector) | Full desert megadune polygon database |
| `dune_database.shp` | Shapefile (vector) | Same database in Shapefile format |
| `dune_attributes.csv` | CSV | Morphometric attribute table (plain text) |
| `dune_attributes.xlsx` | Excel | Morphometric attribute table (formatted) |
| `*.tif` | GeoTIFF (raster) | Derived raster products (DEM, slope, curvature, etc.) |

> **How to download:** Navigate to the **[Releases](../../releases)** page → select the latest release (≥ V1.0) → download the desired files from the *Assets* section.

---

所有公开数据资产均已打包发布在本仓库的 **[Releases 页面](../../releases)**，请前往该页面选择最新版本并从 *Assets* 区块下载所需文件。各文件格式及说明如下表：

| 文件名 | 格式 | 说明 |
|--------|------|------|
| `dune_database.gpkg` | GeoPackage（矢量） | 全沙漠高大沙山面状矢量数据库 |
| `dune_database.shp` | Shapefile（矢量） | 同上，Shapefile 格式 |
| `dune_attributes.csv` | CSV | 沙山形态属性表（纯文本） |
| `dune_attributes.xlsx` | Excel | 沙山形态属性表（带格式） |
| `*.tif` | GeoTIFF（栅格） | 衍生栅格产品（DEM、坡度、曲率等） |

---

## 📖 Data Dictionary — 数据字典

The table below describes every field included in `dune_database.gpkg / .shp` and `dune_attributes.csv / .xlsx`.

下表说明 `dune_database.gpkg / .shp` 及 `dune_attributes.csv / .xlsx` 中每个字段的含义与单位。

| Field Name 字段名 | Type 类型 | Unit 单位 | English Description | 中文说明 |
|-------------------|-----------|-----------|---------------------|----------|
| `Dune_ID` | Integer | — | Unique identifier for each megadune | 沙山唯一标识号 |
| `Partition` | String | — | Sub-region / administrative partition the dune belongs to | 所属区划 / 分区 |
| `Center_X` | Float | ° / m | Geographic centroid X coordinate (longitude or easting) | 地理中心 X 坐标（经度或东向投影坐标） |
| `Center_Y` | Float | ° / m | Geographic centroid Y coordinate (latitude or northing) | 地理中心 Y 坐标（纬度或北向投影坐标） |
| `Density_km2` | Float | count / km² | Spatial density of megadunes per square kilometre | 空间分布密度（个 / 平方公里） |
| `RelHeight` | Float | m | Relative height — vertical difference between crest and surrounding interdune floor | 相对高度（沙山顶与周围丘间低地的高差，单位：米） |
| `Volume` | Float | m³ | Estimated sand volume of the megadune above the interdune baseline | 沙山体积（立方米），基于插值基面以上的砂体积分 |
| `Slope_Mean` | Float | ° | Mean surface slope over the entire dune body | 全沙山体平均坡度（度） |
| `Slope_Max` | Float | ° | Maximum surface slope recorded on the dune | 最大坡度（度） |
| `ReposeArea` | Float | m² | Surface area with slope within the angle-of-repose range (28 °–38 °) | 坡度处于休止角范围（28 °–38 °）的表面积（平方米） |
| `Repose_Pct` | Float | % | Percentage of total surface area that lies within the angle-of-repose range | 休止角面积占总表面积的比例（%） |
| `Curvature` | Float | m⁻¹ | Mean surface curvature (positive = convex, negative = concave) | 表面平均曲率（正值为凸形，负值为凹形） |
| `Strike_Deg` | Float | ° | Azimuth of the main dune crest / long axis, measured clockwise from north (0–180 °) | 主脊线 / 长轴走向方位角（从正北顺时针，0–180 °） |
| `Aspect_Rat` | Float | — | Aspect ratio — ratio of cross-wind width to along-wind length | 宽高比（垂直风向宽度与顺风方向长度之比） |

---

## 📝 Citation & Contact — 引用与联系

### Citation 引用格式

If you use these data in your research, please cite the forthcoming paper (placeholder — update upon publication):

如您在研究中使用了本数据，请引用以下论文（占位符，正式发表后更新）：

```bibtex
@article{chen2025badainjaran,
  author    = {Chen, Feiyi and others},
  title     = {Physics-Informed Differentiable Cellular Automaton for Instance Segmentation
               and 3-D Morphometry of Desert Megadunes: A Case Study of the Badain Jaran Desert},
  journal   = {(Under Review)},
  year      = {2025},
  note      = {Pre-release dataset available at https://github.com/fyichen2023/BadainJaran-Dune-Seg}
}
```

### Contact 联系方式

| | |
|---|---|
| **Maintainer** | Feiyi Chen (陈飞翼) |
| **Affiliation** | *(Please update with your institution)* |
| **E-mail** | *(Please update with your contact e-mail)* |
| **Issues** | Please open a [GitHub Issue](../../issues) for data-related questions |

---

<p align="center">
  <i>Data release V1.0 — Full code to be released upon paper acceptance.</i><br>
  <i>数据版本 V1.0 — 完整代码将在论文接收后正式开源。</i>
</p>
