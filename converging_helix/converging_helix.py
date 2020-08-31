# from: https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ
from math import cos, degrees, pi, sin
from typing import Callable, Tuple


def converging_helix(
    radius: float,
    pitch: float,
    height: float,
    inset: float = 0,
    cvrg_factor: float = 0,
    horz_offset: float = 0,
    vert_offset: float = 0,
    first_t: float = 0,
    last_t: float = 1,
) -> Callable[[float], Tuple[float, float, float]]:
    """
    Returns a function which can be used to create helixes that are
    as simple as a single line to as complex as multifacited 3d solids
    that start at a point then smoothly expand to the solid and then
    smoothly converge back to a point.

    The initial use case is to create triangular or trapazoidal threads
    for nuts and bolts. Invoking converging_helix multiple times with the
    same radius, pitch, inset, first_t, and last_t but with differing values
    for cvrg_factor, horz_offset and vert_offset the final solid will start
    at a point expand to the desired shape and then converge back to a
    point.

    Right now all "illegal parameters" will return Tuple[0, 0, 0]

    TODO: Should we throw an error on "illegal parameters" to converging_helix
          such as, helix_height != 0, pitch != 0, first_t >= cvrg_factor, cvrtFactor <= last_t

    TODO: Should "func" throw an error on "illegal parameters" such as t out of range
    """

    def func(t: float) -> Tuple[float, float, float]:

        x: float = 0
        y: float = 0
        z: float = 0

        # Reduce the height by 2 * inset. Threads start at inset
        # and end at height - inset.
        helix_height: float = height - (2 * inset)
        if (
            helix_height != 0
            and pitch != 0
            and t >= first_t
            and t <= last_t
            and first_t <= cvrg_factor
            and cvrg_factor <= last_t
        ):
            fade_angle: float

            if (cvrg_factor > first_t) and (t <= cvrg_factor):
                # FadeIn, fade_angle is 0 to 90deg so fade_scale is between 0 and 1
                fade_angle = +(pi / 2 * t / cvrg_factor)
            elif (cvrg_factor == 0) or ((t > cvrg_factor) and (t < last_t - cvrg_factor)):
                # No fading set fade_angle to 90deg so sin(fade_angle) == 1
                fade_angle = pi / 2
            else:
                # FadeOut, fade_angle is 90 to 0deg so fade_scale is between 1 and 0
                fade_angle = -((2 * pi) - (pi / 2 * (last_t - t) / cvrg_factor))
            fade_scale: float = sin(fade_angle)

            r: float = radius + (horz_offset * fade_scale)
            a: float = 2 * pi / (pitch / helix_height) * t
            x = r * sin(-a)
            y = r * cos(a)
            z = (helix_height * t) + (vert_offset * fade_scale) + inset

            # print(f"converging_helix.f: {t:.4f}: ({x:.4f}, {y:.4f}, {z:.4f})")
        else:
            # print(f"converging_helix.f: {t:.4f}: (0, 0, 0)")
            pass

        return (x, y, z)

    return func
