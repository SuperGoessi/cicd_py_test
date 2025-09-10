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
    if len(targets) == 0:
        raise ValueError("targets is empty")
    target_sindex = targets.sindex
    dists = []
    for geom in sources:
        possible_matches_index = list(target_sindex.nearest(geom.bounds, 1))[0:1]
        candidate = targets.iloc[possible_matches_index[0]]
        dists.append(geom.distance(candidate))
    return dists


def make_demo_points(n: int = 5) -> gpd.GeoDataFrame:
    pts = [Point(i * 100.0, i * 50.0) for i in range(n)]
    gdf = gpd.GeoDataFrame({"id": list(range(n))}, geometry=pts, crs="EPSG:3857")
    return gdf