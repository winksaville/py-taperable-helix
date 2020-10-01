from dataclasses import dataclass
from math import cos, degrees, pi, sin
from typing import Callable, Optional, Tuple


@dataclass
class Helix:
    """
    This represents a basic Helix. The required attributes are radius,
    pitch and height. Thse attributes create simple single line helix.
    But the primary purpose for Helix is to create a set of helical "wires"
    using non-zero values for taper_rpos, horz_offset and vert_offset to
    define solid helixes that can taper at each end to a point.

    This is useful for creating internal and external threads for nuts and
    bolts.  This is accomplished by invoking helix() multiple times with
    same radius, pitch, taper_rpos, inset_offset, first_t, and last_t.
    But with different HelixLocation radius, horz_offset and vert_offset.

    Each returned function will then generate a helix defining an edge
    of the thread. The edges can be used to make faces and subsequently
    a solid of the thread. This can then be combined with the "core" objects
    which the threads are "attached" using a "union" operator.
    """

    radius: float  #: radius of the basic helix.
    pitch: float  #: pitch of the helix per revolution. I.e the distance between the height of a single "turn" of the helix.
    height: float  #: height of the cyclinder containing the helix.
    taper_out_rpos: float = 0  #: taper_out_rpos: is a decimal number with an inclusive range of 0..1 such that (taper_out_rpos * t_range) defines the t value where tapering out ends, it begins at t == first_t.  A ValueError exception is raised if taper_out_rpos < 0 or > 1 or taper_out_rpos > taper_in_rpos. Default is 0 which is no out taper
    taper_in_rpos: float = 1  #: taper_in_rpos: is a decimal number with an inclusive range of 0..1 such that (taper_in_rpos * t_range) defines the t value where tapering in begins, it ends at t == last_t.  A ValueError exception is raised if taper_out_rpos < 0 or > 1 or taper_out_rpos > taper_in_rpos. Default is 1 which is no in taper.
    inset_offset: float = 0  #: inset_offset: the helix will start at z = inset_offset and will end at z = height - (2 * inset_offset). Default 0.
    first_t: float = 0  #: first_t is the first t value passed to the returned function. Default 0
    last_t: float = 1  #: last_t is the last t value passed to the returned function. Default 1


@dataclass
class HelixLocation:
    radius: Optional[float] = None  #: radis of helix if none h.radius is used
    horz_offset: float = 0  #: horzitional offset added to the radius
    vert_offset: float = 0  #: vertical added to z of radius


def helix(
    h: Helix, hl: Optional[HelixLocation] = None
) -> Callable[[float], Tuple[float, float, float]]:
    """
    This function takes a Helix and optionally a HelixLocation which refines the
    location of the final helix. If HelixLocation is None then the radius is h.radius
    and and horz_offset and vert_offset will be 0. Since it's common for simple
    helixes HelixLocation.radius can also be None and h.radius will be used.

    This function returns a function, f. The funciton f that takes one parameter,
    an inclusive value between h.first_t and h.last_t.  We then define
    t_range=h.last_t-h.first_t and the rel_height=(h.last_t-t)/t_range. furthermore
    when using the h.first_t=0 and h.last_t=1, the defaults, t is rel_height.
    The value returned from f is a tuple(x, y, z) which defines a point
    on the helix defined by Helix.

    Credit: Adam Urbanczyk from cadquery [forum post](https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ)

    :param h: Is the basic heliex to generate.
    :param hl: Is the location for the helix.
    :returns: A function which is passes a value between h.first_t and h.last_t
    and returns a 3D point tuple (x, y, z)
    """
    if h.taper_out_rpos > h.taper_in_rpos:
        raise ValueError(
            f"taper_out_rpos:{h.taper_out_rpos} > taper_in_rpos:{h.taper_in_rpos}"
        )

    if h.taper_out_rpos < 0 or h.taper_out_rpos > 1:
        raise ValueError(f"taper_out_rpos:{h.taper_out_rpos} should be >= 0 and <= 1")

    if h.taper_in_rpos < 0 or h.taper_in_rpos > 1:
        raise ValueError(f"taper_in_rpos:{h.taper_in_rpos} should be >= 0 and <= 1")

    # Being "Tricky" to be flexible
    if hl is None:
        hl = HelixLocation(h.radius)
    elif hl.radius is None:
        hl.radius = h.radius

    # Reduce the height by 2 * inset_offset. Threads start at inset_offset
    # and end at height - inset_offset
    helix_height: float = (h.height - (2 * h.inset_offset))

    # The number or revolutions of the helix within the helix_height
    # set to 1 if pitch or helix_height is 0
    turns: float = h.pitch / helix_height if h.pitch != 0 and helix_height != 0 else 1

    # With this DISABLED points t_range will be negative
    # when h.last_t < h.first_t. This causes rel_height in "f"
    # to be negative and as a consequence # the values
    # generated by "f" will always be the same order.
    # See test_helix_backwards.
    #
    # If we ENABLE the code below and swap the order
    # if h.last_t < h.first_t then test_helix_backwards will
    # fail because the order of points in the resulting
    # array will be in reversed order.
    #
    # if h.last_t < h.first_t:
    #     h.last_t, h.first_t = h.first_t, h.last_t

    t_range: float = h.last_t - h.first_t

    taper_out_range: float = t_range * h.taper_out_rpos
    taper_out_ends: float = h.first_t + taper_out_range if taper_out_range > 0 else min(
        h.first_t, h.last_t
    )

    taper_in_range: float = t_range * (1 - h.taper_in_rpos)
    taper_in_starts: float = h.last_t - taper_in_range if taper_in_range > 0 else max(
        h.first_t, h.last_t
    )

    # print(f"helix: ft={h.first_t:.4f} lt={h.last_t:.4f} tr={t_range:.4f}")
    # print(f"helix: tor={taper_out_range:.4f} toe={taper_out_ends:.4f}")
    # print(f"helix: tir={taper_in_range:.4f} tis={taper_in_starts:.4f}")

    def func(t: float) -> Tuple[float, float, float]:
        """
        Return a tuple(x, y, z)
        :param t: A value between h.first_t .. h.last_t inclusive
        """

        taper_angle: float
        toffset: float = t - h.first_t
        rel_height: float = toffset / t_range if t_range != 0 else 0

        # print(f"f:  t={t:.4f}")
        # print(f"f:  tor={taper_out_range:.4f} toe={taper_out_ends:.4f}")
        # print(f"f:  tir={taper_in_range:.4f} tis={taper_in_starts:.4f}")
        if t < taper_out_ends:
            # Taper out from a point, taper_scale will be between 0 and 1
            # This code path is used when t < taper_out and this helix
            # will smoothly taper from a point as taper angle starts at 0
            # and increases to p/2.
            # print(f"f:  out t={t:.4f} < taper_out_ends:{taper_out_ends}")
            taper_angle = pi / 2 * (t - h.first_t) / taper_out_range
        elif t <= taper_in_starts:
            # No tapering, taper_scale == 1
            # print(f"f:  no  t={t:.4f} >= taper_out_ends:{taper_out_ends} <= taper_in_starts:{taper_in_starts}")
            taper_angle = pi / 2
        else:
            # This code path is used when t > taper_in_starts and the this helix
            # will smoothly taper to a point as taper angle starts at p/2
            # and decrease to 0.
            # print(f"f:  in  t={t:.4f} > taper_in_starts:{taper_in_starts}")
            taper_angle = pi / 2 * (h.last_t - t) / taper_in_range

        # print(f"taper_angle={taper_angle}")
        taper_scale: float = sin(taper_angle)

        r: float = hl.radius + (hl.horz_offset * taper_scale)
        a: float = (2 * pi / turns) * rel_height

        x: float = r * sin(-a)
        y: float = r * cos(a)
        z: float = (
            (helix_height * (rel_height if h.pitch != 0 else 1))
            + (hl.vert_offset * taper_scale)
            + h.inset_offset
        )

        result: Tuple[float, float, float] = (x, y, z)
        # print(f"f:  tpa={degrees(taper_angle):.4f} tps={taper_scale:.4f} r={r:.4f} a={degrees(a):.4f}")
        # print(f"f:  t={t:.4f} toffset={toffset:.4f} rh={rel_height:.4f} result={result}")
        return result

    return func
