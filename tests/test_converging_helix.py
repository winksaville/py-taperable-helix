#!/usr/bin/env python3
import ast
import sys
from math import isclose
from typing import Callable, List, Tuple

import plotly.express as px
import pytest
from numpy import arange

from converging_helix import converging_helix as chelix

# Default abs_tol
defaultAt = 1e-6

# Data directory string
data_dir_str = "tests/data/"


def isclose_tuple(
    v1: Tuple[float, ...],
    v2: Tuple[float, ...],
    rel_tol: float = 1e-9,
    abs_tol: float = defaultAt,
) -> bool:
    # print(f"isclose_tuple: v1={v1} v2={v2}")
    return all(
        [isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol) for a, b in zip(v1, v2)]
    )


def isclose_points(
    result: List[Tuple[float, float, float]],
    expected: List[Tuple[float, float, float]],
    rel_tol: float = 1e-9,
    abs_tol: float = defaultAt,
) -> bool:
    # print(f"isclose_points: result={result} expected={expected}")
    return all([isclose_tuple(v1, v2) for v1, v2 in zip(result, expected)])


def generate_points(
    f: Callable[[float], Tuple[float, float, float]],
    first_t: float,
    last_t: float,
    inc: float,
) -> List[Tuple[float, float, float]]:
    l: List[Tuple[float, float, float]] = list(map(f, arange(first_t, last_t, inc)))
    # print(f"generate_points: len(l)={len(l)}")
    l.append(f(last_t))
    # print(f"generate_points: len(1)={len(l)} first_t={first_t} last_t={last_t} l={l}")
    return l


def write_points(
    fname: str, points: List[Tuple[float, float, float]],
) -> List[Tuple[float, float, float]]:
    with open(fname + ".txt", "w") as f:
        for x, y, z in points:
            f.writelines(f"{x}, {y}, {z},\n")


def read_points(fname: str) -> List[Tuple[float, float, float]]:
    points: List[Tuple[float, float, float]]
    with open(fname + ".txt", "r") as f:
        points = [ast.literal_eval(line) for line in f]
    return points


def view(
    title: str,
    points: List[Tuple[float, float, float]],
    first_t: float,
    last_t: float,
    inc: float,
) -> None:
    # print(f"view: points={points}")
    fig = px.line_3d(
        title=title,
        x=[x for x, _, _ in points],
        y=[y for _, y, _ in points],
        z=[z for _, _, z in points],
    )
    fig.layout.scene.camera.projection.type = "orthographic"
    fig.show()


def doit(
    func_name: str,
    points: List[Tuple[float, float, float]],
    first_t: float,
    last_t: float,
    inc: float,
    viewable: bool = False,
    generate: bool = False,
) -> None:
    fname: str = data_dir_str + func_name
    if generate:
        write_points(fname, points)
    if viewable:
        view(func_name, points, first_t, last_t, inc)
    expected = read_points(fname)
    assert points == expected


def test_radius_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    print(f"{func_name}: view={view} generate={generate}")
    first_t = 0
    last_t = 1
    inc = 0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=0,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )
    # A vertical line starting at 0 ending at 1
    first_pt = (0, 0, 0)
    last_pt = (0, 0, 1)
    assert points[0] == first_pt
    assert points[-1] == last_pt
    assert all(
        [
            (pt[0], pt[1], 0) == (0, 0, 0) and (pt >= first_pt) and (pt <= last_pt)
            for pt in points
        ]
    )


def test_radius_0_neg_1_pos_1_t(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = -1
    last_t = 1
    inc = 0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=0,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )
    # A vertical line starting at 0 ending at 1
    first_pt = (0, 0, 0)
    last_pt = (0, 0, 1)
    assert points[0] == first_pt
    assert points[-1] == last_pt
    assert all(
        [
            (pt[0], pt[1], 0) == (0, 0, 0) and (pt >= first_pt) and (pt <= last_pt)
            for pt in points
        ]
    )


def test_radius_0_pos_0_neg_1_t(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = -1
    inc = -0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=0,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )

    # A vertical line starting at 1 ending at 0
    first_pt = (0, 0, 0)
    last_pt = (0, 0, 1)
    assert points[0] == first_pt
    assert points[-1] == last_pt
    assert all(
        [
            (pt[0], pt[1], 0) == (0, 0, 0) and (pt >= first_pt) and (pt <= last_pt)
            for pt in points
        ]
    )


def test_radius_0_neg_2_neg_1_t(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = -2
    last_t = -1
    inc = 0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=0,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )

    # A vertical line starting at 1 ending at 0
    first_pt = (0, 0, 0)
    last_pt = (0, 0, 1)
    assert points[0] == first_pt
    assert points[-1] == last_pt
    assert all(
        [
            (pt[0], pt[1], 0) == (0, 0, 0) and (pt >= first_pt) and (pt <= last_pt)
            for pt in points
        ]
    )


def test_radius_0_neg_1_neg_2_t(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = -1
    last_t = -2
    inc = -0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=0,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )

    # A vertical line starting at 1 ending at 0
    first_pt = (0, 0, 0)
    last_pt = (0, 0, 1)
    assert points[0] == first_pt
    assert points[-1] == last_pt
    assert all(
        [
            (pt[0], pt[1], 0) == (0, 0, 0) and (pt >= first_pt) and (pt <= last_pt)
            for pt in points
        ]
    )


def test_radius_0_neg_height(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = 1
    inc = 0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=-1,
        cvrg_factor=0,
        inset_offset=0,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )

    # A vertical line starting at 0 ending at -1
    first_pt = (0, 0, 0)
    last_pt = (0, 0, -1)
    assert points[0] == first_pt
    assert points[-1] == last_pt
    assert all(
        [
            (pt[0], pt[1], 0) == (0, 0, 0) and (pt <= first_pt) and (pt >= last_pt)
            for pt in points
        ]
    )


def test_radius_0_t_pos_0_neg_1_height_neg_1(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = -1
    inc = -0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=-1,
        cvrg_factor=0,
        inset_offset=0,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )

    # A vertical line starting at 0 ending at -1
    first_pt = (0, 0, 0)
    last_pt = (0, 0, -1)
    assert points[0] == first_pt
    assert points[-1] == last_pt
    assert all(
        [
            (pt[0], pt[1], 0) == (0, 0, 0) and (pt <= first_pt) and (pt >= last_pt)
            for pt in points
        ]
    )


def test_radius_0_first_0_last_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = 0
    inc = 0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=0,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )

    # A point at origin
    assert len(points) == 1
    assert points[0] == (0, 0, 0)


def test_radius_0_inset_1(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = 0
    inc = 0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=1,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )

    # A point at origin (0, 0, 1)
    assert len(points) == 1
    assert points[0] == (0, 0, 1)


def test_radius_0_first_0_last_0_inset_neg_1(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = 0
    inc = 0.1
    f = chelix(
        radius=0,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=-1,
        horz_offset=0,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    print(f"{func_name}: first_t={first_t} last_t={last_t} inc={inc}")
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )

    # A point at origin (0, 0, -1)
    assert len(points) == 1
    assert points[0] == (0, 0, -1)


# def test_radius_0_others_non_zero_neg_100_pos_100_t(view, generate):
#     func_name: str = sys._getframe().f_code.co_name
#     first_t = -100
#     last_t = 100
#     inc = 1
#     f = chelix(
#         radius=0,
#         pitch=1,
#         height=1,
#         cvrg_factor=0.1,
#         inset_offset=0.1,
#         horz_offset=1,
#         vert_offset=1,
#         first_t=first_t,
#         last_t=last_t,
#     )
#     points = generate_points(f, first_t, last_t, inc)
#     doit(
#         func_name,
#         points,
#         first_t,
#         last_t,
#         inc,
#         viewable=view,
#         generate=generate,
#     )


def test_pitch_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = -100
    last_t = 100
    inc = 1
    f = chelix(
        radius=1,
        pitch=0,
        height=1,
        cvrg_factor=0.1,
        inset_offset=0.1,
        horz_offset=1,
        vert_offset=1,
        first_t=first_t,
        last_t=last_t,
    )
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )


def test_pitch_negative_near_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = -100
    last_t = 100
    inc = 1
    f = chelix(
        radius=1,
        pitch=0,
        height=1,
        cvrg_factor=0.1,
        inset_offset=0.1,
        horz_offset=1,
        vert_offset=1,
        first_t=first_t,
        last_t=last_t,
    )
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )


def test_height_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = -100
    last_t = 100
    inc = 1
    f = chelix(
        radius=1,
        pitch=1,
        height=0,
        cvrg_factor=0.1,
        inset_offset=0.1,
        horz_offset=1,
        vert_offset=1,
        first_t=first_t,
        last_t=last_t,
    )
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )


def test_horz_offset_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = 1
    inc = 0.01
    f = chelix(
        radius=1,
        pitch=1,
        height=1,
        cvrg_factor=0.1,
        inset_offset=0.1,
        horz_offset=0,
        vert_offset=1,
        first_t=first_t,
        last_t=last_t,
    )
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )


def test_vert_offset_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = 1
    inc = 0.01
    f = chelix(
        radius=1,
        pitch=1,
        height=1,
        cvrg_factor=0.1,
        inset_offset=0.1,
        horz_offset=1,
        vert_offset=0,
        first_t=first_t,
        last_t=last_t,
    )
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )


def test_inset_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = 1
    inc = 0.01
    f = chelix(
        radius=1,
        pitch=1,
        height=1,
        cvrg_factor=0.1,
        inset_offset=0,
        horz_offset=1,
        vert_offset=1,
        first_t=first_t,
        last_t=last_t,
    )
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )


def test_cvrg_factor_0(view, generate):
    func_name: str = sys._getframe().f_code.co_name
    first_t = 0
    last_t = 1
    inc = 0.01
    f = chelix(
        radius=1,
        pitch=1,
        height=1,
        cvrg_factor=0,
        inset_offset=0.1,
        horz_offset=1,
        vert_offset=1,
        first_t=first_t,
        last_t=last_t,
    )
    points = generate_points(f, first_t, last_t, inc)
    doit(
        func_name, points, first_t, last_t, inc, viewable=view, generate=generate,
    )


def main():
    # For debugging, use `make t` or `pytest` to actually run the tests
    pass


if __name__ == "__main__":
    main()
