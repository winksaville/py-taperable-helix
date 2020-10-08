#!/usr/bin/env python3
import argparse
from typing import List, Tuple

import plotly.express as px
import plotly.graph_objs as go
from numpy import linspace

from taperable_helix import Helix, HelixLocation


def helical_line(
    radius: float = 5, pitch: float = 2, height: float = 6, num_points: int = 100
) -> List[Tuple[float, float, float]]:
    h: Helix = Helix(radius=radius, pitch=pitch, height=height)
    f = h.helix()
    points = list(map(f, linspace(start=0, stop=1, num=num_points, dtype=float)))
    # print(f"helical_line: points={points}")
    return points


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

    points = helical_line()
    fig = px.line_3d(
        # title="Helical Line",
        x=[x for x, _, _ in points],
        y=[y for _, y, _ in points],
        z=[z for _, _, z in points],
    )
    fig.layout.scene.camera.projection.type = "orthographic"

    if args.no_show:
        args.show = False

    if args.show:
        fig.show()

    if args.write:
        try:
            # fname = "data/helical_line.html"
            # fig.write_html(fname)
            # print(f"wrote: {fname}")

            fname = "data/helical_line.webp"
            fig.write_image(fname)
            print(f"wrote: {fname}")
        except Exception:
            print("Unable to write files; run from project root")
