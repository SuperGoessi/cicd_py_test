import geopandas as gpd
from shapely.geometry import Point
from geoprocessing import make_demo_points, buffer_features, union_area, nearest_distance


def test_buffer_and_area():
    gdf = make_demo_points(3)  # (0,0), (100,50), (200,100) in EPSG:3857
    out = buffer_features(gdf, 10.0)
    assert len(out) == 3
    area = union_area(out)
    assert area > 900.0


def test_nearest_distance():
    src = gpd.GeoSeries([Point(0, 0), Point(0, 10)], crs="EPSG:3857")
    tgt = gpd.GeoSeries([Point(5, 0)], crs="EPSG:3857")
    dists = nearest_distance(src, tgt)
    assert len(dists) == 2
    assert abs(dists[0] - 5.0) < 1e-6
    assert abs(dists[1] - (125 ** 0.5)) < 1e-6