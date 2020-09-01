#!/usr/bin/env python3
import argparse

import plotly.express as px
from numpy import arange

from converging_helix import converging_helix as chelix

# Create a function which generates a 3d tuple(x,y,z)
# when invoked with a parameter between 0 .. 1 inclusive.
# The returned tuple will be a point on the helix.
hf = chelix(radius=5, pitch=2, height=2)

# Create a list of tuples for each point on the helix
data = list(map(hf, arange(0.0, 1.0 + 0.01, 0.01)))

fig = px.line_3d(
    x=[x for x, _, _ in data], y=[y for _, y, _ in data], z=[z for _, _, z in data],
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
