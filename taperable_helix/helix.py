from math import cos, degrees, pi, sin
from typing import Callable, Tuple


def helix(
    radius: float,
    pitch: float,
    height: float,
    taper_out_rpos: float = 0,
    taper_in_rpos: float = 0,
    inset_offset: float = 0,
    horz_offset: float = 0,
    vert_offset: float = 0,
    first_t: float = 0,
    last_t: float = 1,
) -> Callable[[float], Tuple[float, float, float]]:
    """
    Returns a function, f. The funciton f takes one parameter,
    an inclusive value between first_t and last_t.  We can then define
    t_range=last_t-first_t and the rel_height=(last_t-t)/t_range. furthermore
    when using the first_t=0 and last_t=1, the defaults, t is rel_height.
    The value returned from f is a tuple(x, y, z) which defines a point
    on the helix defined by the other parameters.

    The helix() function has radius, pitch and height parameters to define a
    basic helix. Using just those parameters you can create simple single
    line helixes. But the primary purpose for helix() is to create a set
    of helical "wires" using non-zero values for taper_rpos, horz_offset and
    vert_offset to define solid helixes that can taper at each end to a point.
    This is useful for creating internal and external threads for nuts and
    bolts.  This is accomplished by invoking helix() multiple times with
    same radius, pitch, taper_rpos, inset_offset, first_t, and last_t.
    But with differing values for  horz_offset and vert_offset. And then
    using the returned functions to define the helical edges of the thread.

    Credit: Adam Urbanczyk from cadquery [forum post](https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ)

    :param radius: of the basic helix.
    :param pitch: of pitch of the helix per revolution. I.e the distance
        between the height of a single "turn" of the helix.
    :param height: of the cyclinder containing the helix.
    :param taper_out_rpos: is a decimal number with an inclusive range
        of 0..1 such that (taper_out_rpos * t_range) defines the
        t value where tapering out ends, it begins at t == first_t.
        A ValueError exception is raised if taper_out_rpos < 0 or > 1 or
        taper_out_rpos > taper_in_rpos.
    :param taper_in_rpos: is a decimal number with an inclusive range
        of 0..1 such that (taper_in_rpos * t_range) defines the
        t value where tapering in begins, it ends at t == last_t.
        A ValueError exception is raised if taper_out_rpos < 0 or > 1 or
        taper_out_rpos > taper_in_rpos.
    :param inset_offset: the helix will start at z = inset_offset and will end
        at z = height - (2 * inset_offset).
    :param horz_offset: is added to the nomimal radius of the helix.
    :param vert_offset: is added to the nonimal z location of the helix
    :param first_t: is the first t value passed to the returned function
    :param last_t: is the last t value passed to the returned function
    """
    if taper_out_rpos > taper_in_rpos:
        raise ValueError(
            f"taper_out_rpos:{taper_out_rpos} > taper_in_rpos:{taper_in_rpos}"
        )

    if taper_out_rpos < 0 or taper_out_rpos > 1:
        raise ValueError(f"taper_out_rpos:{taper_out_rpos} should be >= 0 and <= 1")

    if taper_in_rpos < 0 or taper_in_rpos > 1:
        raise ValueError(f"taper_in_rpos:{taper_in_rpos} should be >= 0 and <= 1")

    # Reduce the height by 2 * inset_offset. Threads start at inset_offset
    # and end at height - inset_offset
    helix_height: float = (height - (2 * inset_offset))

    # The number or revolutions of the helix within the helix_height
    # set to 1 if pitch or helix_height is 0
    turns: float = pitch / helix_height if pitch != 0 and helix_height != 0 else 1

    t_range: float = last_t - first_t

    taper_out_range: float = t_range * taper_out_rpos
    taper_out_ends: float = first_t + taper_out_range

    taper_in_range: float = t_range * (1 - taper_in_rpos)
    taper_in_starts: float = last_t - taper_in_range

    print(f"helix: ft={first_t} lt={last_t} tr={t_range}")
    print(f"helix: tor={taper_out_range} toe={taper_out_ends}")
    print(f"helix: tir={taper_in_range} tis={taper_in_starts}")

    def func(t: float) -> Tuple[float, float, float]:
        """
        Return a tuple(x, y, z)
        :param t: A value between first_t .. last_t inclusive
        """

        x: float = 0
        y: float = 0
        z: float = 0

        taper_angle: float
        taper_scale: float
        toffset: float = t - first_t
        rel_height: float = toffset / t_range if t_range != 0 else 0

        if t < taper_out_ends:
            # Taper out from a point, taper_scale will be between 0 and 1
            # This code path is used when t < taper_out and this helix
            # will smoothly taper from a point as taper angle starts at 0
            # and increases to p/2.
            print(f"out t={t} < taper_out_ends:{taper_out_ends}")
            taper_angle = pi / 2 * (t - first_t) / taper_out_range
        elif (t >= taper_out_ends) and (t < taper_in_starts):
            # No tapering, taper_scale == 1
            print(f"no  t={t} >= taper_out_ends:{taper_out_ends} <= taper_in_starts:{taper_in_starts}")
            taper_angle = pi / 2
        else:
            # This code path is used when t > taper_in_starts and the this helix
            # will smoothly taper to a point as taper angle starts at p/2
            # and decrease to 0.
            print(f"in  t={t} > taper_in_starts:{taper_in_starts}")
            taper_angle = pi / 2 * (last_t - t) / taper_in_range

        print(f"taper_angle={taper_angle}")
        taper_scale = sin(taper_angle)

        r: float = radius + (horz_offset * taper_scale)
        a: float = (2 * pi / turns) * rel_height

        x = r * sin(-a)
        y = r * cos(a)
        z = (
            (helix_height * (rel_height if pitch != 0 else 1))
            + (vert_offset * taper_scale)
            + inset_offset
        )

        result = (x, y, z)
        print(f"f: tpa={taper_angle} tps={taper_scale} r={r} a={a}")
        print(f"f: t={t} toffset={toffset} rh={rel_height} result={result}")
        return result

    return func
