from __future__ import annotations
import argparse
import sys
import geopandas as gpd
from pathlib import Path
from geoprocessing import buffer_features, union_area, make_demo_points, nearest_distance


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="GeoPandas run: buffer/nearest dist/area"
    )
    p.add_argument("--input", type=str, default="", help="inport(GeoJSON/GPKG/Shapefile)。use demo data if null。")
    p.add_argument("--buffer", type=float, default=50.0, help="buffer distance（unit=projection unit）")
    p.add_argument("--output", type=str, default="output.geojson", help="path（GeoJSON or GPKG）")
    p.add_argument("--nearest-demo", action="store_true", help="nearest dist")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.input:
        gdf = gpd.read_file(args.input)
    else:
        gdf = make_demo_points(6)

    gdf_buf = buffer_features(gdf, args.buffer)
    total_area = union_area(gdf_buf)

    if args.nearest_demo:
        targets = gdf.copy()
        targets["geometry"] = targets.geometry.translate(xoff=300, yoff=0)
        dists = nearest_distance(gdf.geometry, targets.geometry)
        gdf_buf["nearest_demo_dist"] = dists


    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    gdf_buf.to_file(out_path, driver="GeoJSON" if out_path.suffix.lower() == ".geojson" else None)

    print(f"[OK] Wrote: {out_path}")
    print(f"[INFO] Buffer distance: {args.buffer}")
    print(f"[INFO] Union area: {total_area:.3f}")
    if args.nearest_demo:
        print(f"[INFO] First 3 nearest distances: {gdf_buf['nearest_demo_dist'][:3].tolist()}")


if __name__ == "__main__":
    sys.exit(main())