#!/usr/bin/env python3
import argparse

import plotly.express as px
import plotly.graph_objs as go
from numpy import arange

from taperable_helix import helix

radius = 1
pitch = 1
height = 1
inset_offset = 0.0
cvrg_factor = 0.5
first_t = 0
last_t = 1
inc = 0.01

# Create three helixes showing the fading
fL = helix(
    radius=radius,
    pitch=pitch,
    height=height,
    cvrg_factor=cvrg_factor,
    inset_offset=inset_offset,
    horz_offset=0,
    vert_offset=+0.1,
    first_t=first_t,
    last_t=last_t,
)

fM = helix(
    radius=radius,
    pitch=pitch,
    height=height,
    cvrg_factor=cvrg_factor,
    inset_offset=inset_offset,
    horz_offset=0.2,
    vert_offset=0,
    first_t=first_t,
    last_t=last_t,
)

fU = helix(
    radius=radius,
    pitch=pitch,
    height=height,
    cvrg_factor=cvrg_factor,
    inset_offset=inset_offset,
    horz_offset=0,
    vert_offset=-0.1,
    first_t=first_t,
    last_t=last_t,
)

# Create a list of tuples for each point on the helix
data_fL = list(
    map(fL, arange(first_t, last_t + inc, inc))
)  # + 10, 10))) # + 0.01, 0.01)))
data_fL.append(fL(last_t))
data_fM = list(
    map(fM, arange(first_t, last_t + inc, inc))
)  # + 10, 10))) # + 0.01, 0.01)))
data_fM.append(fM(last_t))
data_fU = list(
    map(fU, arange(first_t, last_t + inc, inc))
)  # + 10, 10))) # + 0.01, 0.01)))
data_fU.append(fU(last_t))

fig = go.Figure(
    layout_title_text="Helical Triangle",
    layout_scene_camera_projection_type="orthographic",
)
fig.add_trace(
    go.Scatter3d(
        # Extract x, y, z
        x=[x for x, _, _ in data_fL],
        y=[y for _, y, _ in data_fL],
        z=[z for _, _, z in data_fL],
        mode="lines",
    )
)
fig.add_trace(
    go.Scatter3d(
        # Extract x, y, z
        x=[x for x, _, _ in data_fM],
        y=[y for _, y, _ in data_fM],
        z=[z for _, _, z in data_fM],
        mode="lines",
    )
)
fig.add_trace(
    go.Scatter3d(
        # Extract x, y, z
        x=[x for x, _, _ in data_fU],
        y=[y for _, y, _ in data_fU],
        z=[z for _, _, z in data_fU],
        mode="lines",
    )
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
