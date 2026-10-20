"""Land outlines for the Navigators maps: Natural Earth 1:110m countries
(public domain, tools/data/ne-LICENSE.md). The file is the copy bundled in the
geopandas 0.14.4 wheel (geopandas/datasets/naturalearth_lowres/
naturalearth_lowres.shp, 180744 bytes, sha256 1f689e60...d533ce12; wheel
sha256 3bb6473c...c99689aa on PyPI), kept in tools/data/naturalearth_lowres.shp
so a build needs no download, no /tmp and no pyshp. It used to be fetched with
pip into /tmp on first use and read with pyshp; this reads the same polygon
records with the standard library, so the rings, and the maps, are the same."""
import os, struct
NE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "naturalearth_lowres.shp")
def rings():
    """Every outer and inner ring as a list of (lon, lat)."""
    b = open(NE, "rb").read()
    out, at = [], 100                                    # the file header is 100 bytes
    while at < len(b):
        size = struct.unpack(">i", b[at + 4:at + 8])[0] * 2   # record content length, in 16-bit words
        rec, at = b[at + 8:at + 8 + size], at + 8 + size
        if struct.unpack("<i", rec[:4])[0] != 5:            # polygons only (a null shape has no rings)
            continue
        nparts, npts = struct.unpack("<2i", rec[36:44])     # after the type and the bounding box
        parts = list(struct.unpack("<%di" % nparts, rec[44:44 + 4 * nparts])) + [npts]
        xy = struct.unpack("<%dd" % (2 * npts), rec[44 + 4 * nparts:44 + 4 * nparts + 16 * npts])
        points = list(zip(xy[0::2], xy[1::2]))
        for a, c in zip(parts[:-1], parts[1:]):
            out.append(points[a:c])
    return out
