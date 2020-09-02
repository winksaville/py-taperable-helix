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
    as simple as a single line or be multiple helixes that start at
    a point then smoothly expand to the solid and then smoothly
    converge back to a point.

    The initial use case is to create triangular or trapazoidal threads
    for nuts and bolts. Invoking converging_helix multiple times with the
    same radius, pitch, inset, first_t, and last_t but with differing values
    for cvrg_factor, horz_offset and vert_offset the final solid will start
    at a point expand to the desired shape and then converge back to a
    point.

    :param radius: of the basic helix.
    :param pitch: of pitch of the helix per revolution.
    :param height: of the cyclinder containing the helix.
    :param inset: the top and bottom of the helicial
    cyclinder where the helix actually starts.
    :param cvrg_factor: if cvrg_factor is 0 no fading occurs
    ortherise cvrg_factor is the percentage of the range of t that fades occur
    at the begining and end of that range.
    """
    # Reduce the height by 2 * inset. Threads start at inset
    # and end at height - inset.
    if inset < 0:
        raise ValueError("inset must be >= 0")

    helix_height: float = (abs(height) - (2 * inset))
    if helix_height <= 0:
        raise ValueError(f"(abs(height)={abs(height)}) < ((2 * inset)={2 * inset}), it must be >=")
    helix_height *= -1 if height < 1 else 1
    turns: float = pitch / helix_height

    if cvrg_factor > 0.5:
        raise ValueError("cvrg_factor={cvrg_factor} > 0.5, should 0 .. 0.5 inclusive")

    t_range: float = last_t - first_t
    if (t_range <= 0):
        raise ValueError("last_t={last_t} <= first_t={first_t}")


    fade_range: float = 0
    if cvrg_factor > 0:
        fade_range = (last_t - first_t) * cvrg_factor

    fade_in_mark: float = first_t + fade_range
    fade_out_mark: float = last_t - fade_range

    def func(t: float) -> Tuple[float, float, float]:
        """
        Return a tuple(x, y, z)
        :param t: A value between first_t .. last_t inclusive
        """

        x: float = 0
        y: float = 0
        z: float = 0

        fade_angle: float
        to: float = t - first_t

        if (fade_range > 0) and (t < fade_in_mark):
            # FadeIn, fade_angle is 0 to 90deg so fade_scale is between 0 and 1
            fade_angle = +(pi / 2 * (t - first_t) / fade_range)
        elif (fade_range == 0) or (
            (t >= fade_in_mark) and (t < fade_out_mark)
        ):
            # No fading set fade_angle to 90deg so sin(fade_angle) == 1
            fade_angle = pi / 2
        else:
            # FadeOut, fade_angle is 90 to 0deg so fade_scale is between 1 and 0
            fade_angle = -((2 * pi) - (pi / 2 * (last_t - t) / fade_range))
        fade_scale: float = sin(fade_angle)

        r: float = radius + (horz_offset * fade_scale)
        a: float = (2 * pi / turns) * (to / t_range)

        x = r * sin(-a)
        y = r * cos(a)
        z = (helix_height * t) + (vert_offset * fade_scale) + inset


        result = (x, y, z)
        return result

    return func
