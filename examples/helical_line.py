#!/usr/bin/env python3
import argparse

import plotly.express as px
import plotly.graph_objs as go
from numpy import arange

from converging_helix import converging_helix as chelix

# Create a function which returns tuple(x,y,z) when
# invoked with a parameter between 0 .. 1 inclusive.
# The returned tuple will be a point on the helix.
inc = 0.01
f = chelix(radius=5, pitch=2, height=6)
l = list(map(f, arange(0, 1 + inc, inc)))
fig = px.line_3d(
    x=[x for x, _, _ in l],
    y=[y for _, y, _ in l],
    z=[z for _, _, z in l],
)

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

    if args.no_show:
        args.show = False

    if args.show:
        fig.show()

    if args.write:
        try:
            fname = "data/helical_line.html"
            fig.write_html(fname)
            print(f"wrote: {fname}")

            fname = "data/helical_line.webp"
            fig.write_image(fname)
            print(f"wrote: {fname}")
        except Exception:
            print("Unable to write files; run from project root")
