#!/usr/bin/env python3
import argparse
from typing import List, Tuple

import plotly.express as px
import plotly.graph_objs as go
from numpy import linspace

from taperable_helix import helix


def helical_triangle(
    radius: float = 1,
    pitch: float = 2,
    height: float = 4,
    num_points: int = 100,
    tri_height: float = 0.2,
    tri_width: float = 0.2,
) -> (
    List[Tuple[float, float, float]],
    List[Tuple[float, float, float]],
    List[Tuple[float, float, float]],
):
    taper_rpos = 0.1
    first_t = 0
    last_t = 1

    # Create three helixes that taper to a point
    fU = helix(radius, pitch, height, taper_rpos=taper_rpos, vert_offset=tri_height / 2)
    points_fU = list(map(fU, linspace(first_t, last_t, num=100, dtype=float)))

    fM = helix(radius, pitch, height, taper_rpos=taper_rpos, horz_offset=tri_width)
    points_fM = list(map(fM, linspace(first_t, last_t, num=100, dtype=float)))

    fL = helix(
        radius, pitch, height, taper_rpos=taper_rpos, vert_offset=-tri_height / 2
    )
    points_fL = list(map(fL, linspace(first_t, last_t, num=100, dtype=float)))
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
        "-w", "--write", help="Write image and html files", action="store_true",
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
