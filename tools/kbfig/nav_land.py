"""Land outlines for the Navigators maps: Natural Earth 1:110m countries
(public domain), read from the copy bundled in the geopandas 0.14.4 wheel.
The wheel is fetched with pip on first use, because the usual map CDNs are not
reachable from every build machine. Needs pyshp (pip install pyshp)."""
import os, glob, zipfile, subprocess
NE = "/tmp/ne/naturalearth_lowres.shp"
def _ensure():
    if os.path.exists(NE):
        return
    os.makedirs("/tmp/ne", exist_ok=True)
    if not glob.glob("/tmp/gpd/geopandas-0.14.4-*.whl"):
        subprocess.check_call(["pip", "download", "-q", "--no-deps", "geopandas==0.14.4", "-d", "/tmp/gpd"])
    z = zipfile.ZipFile(glob.glob("/tmp/gpd/geopandas-0.14.4-*.whl")[0])
    for n in z.namelist():
        if "naturalearth_lowres/" in n:
            open("/tmp/ne/" + n.split("/")[-1], "wb").write(z.read(n))
def rings():
    """Every outer and inner ring as a list of (lon, lat)."""
    _ensure()
    import shapefile
    out = []
    for sh in shapefile.Reader(NE).shapes():
        parts = list(sh.parts) + [len(sh.points)]
        for a, b in zip(parts[:-1], parts[1:]):
            out.append(sh.points[a:b])
    return out
