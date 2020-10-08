#!/usr/bin/env python3
import argparse
from typing import List, Tuple

import plotly.express as px
import plotly.graph_objs as go
from numpy import linspace

from taperable_helix import Helix, HelixLocation


def helical_triangle(
    radius: float = 1,
    pitch: float = 2,
    height: float = 4,
    num_points: int = 100,
    tri_height: float = 0.2,
    tri_width: float = 0.2,
) -> Tuple[
    List[Tuple[float, float, float]],
    List[Tuple[float, float, float]],
    List[Tuple[float, float, float]],
]:

    # Create three helixes that taper to a point

    # Create the base Helix
    h: Helix = Helix(
        radius=radius, pitch=pitch, height=height, taper_out_rpos=0.1, taper_in_rpos=0.9
    )

    # The Upper points, horz_offset defaults to 0
    fU = h.helix(HelixLocation(vert_offset=tri_height / 2))
    points_fU = list(map(fU, linspace(h.first_t, h.last_t, num=100, dtype=float)))

    # The Lower points, again horz_offset defaults to 0
    fL = h.helix(HelixLocation(vert_offset=-tri_height / 2))
    points_fL = list(map(fL, linspace(h.first_t, h.last_t, num=100, dtype=float)))

    # The Middle point, change vert_offset to 0
    fM = h.helix(HelixLocation(horz_offset=tri_width))
    points_fM = list(map(fM, linspace(h.first_t, h.last_t, num=100, dtype=float)))

    return (points_fU, points_fM, points_fL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--show",
        help="show result in browser (default)",
        default=True,
        action="store_true",
    )
    parser.add_argument(
        "-ns",
        "--no-show",
        help="do not show result",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-w",
        "--write",
        help="Write image and html files",
        action="store_true",
    )
    args = parser.parse_args()

    # Create the points for the helixes
    points_fU, points_fM, points_fL = helical_triangle()

    # Create a plotly figure add three traces
    fig = go.Figure(
        # layout_title_text="Helical Triangle",
        layout_scene_camera_projection_type="orthographic",
    )
    fig.add_trace(
        go.Scatter3d(
            # Extract x, y, z
            x=[x for x, _, _ in points_fL],
            y=[y for _, y, _ in points_fL],
            z=[z for _, _, z in points_fL],
            mode="lines",
            name="Lower",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            # Extract x, y, z
            x=[x for x, _, _ in points_fM],
            y=[y for _, y, _ in points_fM],
            z=[z for _, _, z in points_fM],
            mode="lines",
            name="Middle",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            # Extract x, y, z
            x=[x for x, _, _ in points_fU],
            y=[y for _, y, _ in points_fU],
            z=[z for _, _, z in points_fU],
            mode="lines",
            name="Upper",
        )
    )

    if args.no_show:
        args.show = False

    if args.show:
        fig.show()

    if args.write:
        try:
            # fname = "data/helical_tri.html"
            # fig.write_html(fname)
            # print(f"wrote: {fname}")

            fname = "data/helical_tri.webp"
            fig.write_image(fname)
            print(f"wrote: {fname}")
        except Exception:
            print("Unable to write files; run from project root")
