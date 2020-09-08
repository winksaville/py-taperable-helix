from math import cos, degrees, pi, sin
from typing import Callable, Tuple


def helix(
    radius: float,
    pitch: float,
    height: float,
    taper_rpos: float = 0,
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

    Credit: Adam Urbanczyk from cadquery forum post:
        https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ

    :param radius: of the basic helix.
    :param pitch: of pitch of the helix per revolution. I.e the distance
        between the height of a single "turn" of the helix.
    :param height: of the cyclinder containing the helix.
    :param taper_rpos: is a decimal fraction such that taper_rpos * t_range
        defines the values of t where tapering ends and begins or if
        taper_rpos is 0 there is no taper. For example if taper_rpos is 0.10
        then tapering will occur when t is with in the first and last 10% of
        t_range.  A ValueError exception is raised if taper_rpos < 0 or > 0.5.
        TODO: Maybe there should be a taper_in_rpos and taper_out_rpos
    :param inset_offset: the helix will start at z = inset_offset and will end
        at z = height - (2 * inset_offset).
    :param horz_offset: is added to the nomimal radius of the helix.
    :param vert_offset: is added to the nonimal z location of the helix
    :param first_t: is the first t value passed to the returned function
    :param last_t: is the last t value passed to the returned function
    """
    if taper_rpos < 0 or taper_rpos > 0.5:
        raise ValueError("taper_rpos={taper_rpos} should be 0 .. 0.5 inclusive")

    # Reduce the height by 2 * inset_offset. Threads start at inset_offset
    # and end at height - inset_offset
    helix_height: float = (height - (2 * inset_offset))

    # The number or revolutions of the helix within the helix_height
    # set to 1 if pitch or helix_height is 0
    turns: float = pitch / helix_height if pitch != 0 and helix_height != 0 else 1

    t_range: float = last_t - first_t

    taper_range: float = t_range * taper_rpos

    taper_out: float = first_t + taper_range
    taper_in: float = last_t - taper_range

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
        to: float = t - first_t
        rel_height: float = to / t_range if t_range != 0 else 0

        if (taper_range > 0) and (t < taper_out):
            # Taper out from a point, taper_scale will be between 0 and 1
            # This code path is used when t < taper_out and this helix
            # will smoothly taper from a point as taper angle starts at 0
            # and increases to p/2.
            taper_angle = pi / 2 * (t - first_t) / taper_range
        elif (taper_range == 0) or ((t >= taper_out) and (t < taper_in)):
            # No tapering, taper_scale == 1
            taper_angle = pi / 2
        else:
            # This code path is used when t >= taper_in and the this helix
            # will smoothly taper to a point as taper angle starts at p/2
            # and decrease to 0.
            taper_angle = pi / 2 * (last_t - t) / taper_range

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
        # print(f"f: ft={first_t} lt={last_t} rh={rel_height} tr={t_range")
        # print(f"f: tpr={taper_range} tpim={taper_in}") tpom={taper_out}")
        # print(f"f: tpa={taper_angle} tps={taper_scale} r={r} a={a}")
        # print(f"f: t={t} to={to} result={result}")
        return result

    return func
