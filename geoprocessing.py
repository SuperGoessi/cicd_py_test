from __future__ import annotations
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union


def buffer_features(gdf: gpd.GeoDataFrame, distance: float) -> gpd.GeoDataFrame:
    if "geometry" not in gdf:
        raise ValueError("Input GeoDataFrame must have a 'geometry' column.")
    out = gdf.copy()
    out["geometry"] = out.geometry.buffer(distance)
    return out


def union_area(gdf: gpd.GeoDataFrame) -> float:
    geom = unary_union(gdf.geometry)
    return geom.area


def nearest_distance(sources: gpd.GeoSeries, targets: gpd.GeoSeries) -> list[float]:
    if sources.empty:
        return []
    if targets.empty:
        raise ValueError("targets is empty")

    if sources.crs != targets.crs:
        targets = targets.to_crs(sources.crs)

    sources = sources[~sources.is_empty & sources.notna()]
    targets = targets[~targets.is_empty & targets.notna()]

    s = gpd.GeoDataFrame(geometry=sources)
    t = gpd.GeoDataFrame(geometry=targets)

    joined = gpd.sjoin_nearest(s, t, how="left", distance_col="dist")
    return joined["dist"].tolist()


def make_demo_points(n: int = 5) -> gpd.GeoDataFrame:
    pts = [Point(i * 100.0, i * 50.0) for i in range(n)]
    gdf = gpd.GeoDataFrame({"id": list(range(n))}, geometry=pts, crs="EPSG:3857")
    return gdf