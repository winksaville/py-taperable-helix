from math import cos, degrees, pi, sin
from typing import Callable, Tuple


def helix(
    radius: float,
    pitch: float,
    height: float,
    cvrg_factor: float = 0,
    inset_offset: float = 0,
    horz_offset: float = 0,
    vert_offset: float = 0,
    first_t: float = 0,
    last_t: float = 1,
) -> Callable[[float], Tuple[float, float, float]]:
    """
    A taperable helix, thelix, returns a pure function which is nomially
    passed a value between 0 and 1 inclusive and then returns a tuple(x, y, z)
    which will be a point on the desired helix.

    A helix can be as simple as a single line or be a set of helical "wires"
    which define a "solid" that can start at a point and the smoothly expand
    to the desired "solid" and then smoothly taper back to a point.

    The nomial use case is to create triangular or trapazoidal threads
    for nuts and bolts. This is accomplished by invoking converging_helix
    multiple times with the same radius, pitch, cvrg_factor, inset_offset,
    first_t, and last_t but with differing values for  horz_offset and
    vert_offset. The returned functions are then invoked over with the desired
    values and the returned points will all start at the same point then
    expand to the sectional shape and then all taper back to the ending point.

    Nomially the helix begins on the xy plane with specified radius, pitch
    and height. The additional parameters, cvrg_factor and xxx_offset values
    modify the helixes shape. The first_t and last_t define the inclusive
    range of values passed as the "t" parameter to the returned function.

    The default values of first_t and last_t are 0 and 1. If first_t == last_t
    then it is assumed the returned function will only be invoked with value
    defined values in the inclusive range of first_t to last_t. The expression,
    rel_t = t / (last_t - first_t), defines the relative t value which is used
    to define the location of where tapering starts and stops. If for some
    reason (last_t - first_t) is 0 then rel_t will be 1 and it is assumed the
    returned function will be called with only first_t. The returned point will
    at the origin + any xxx_offsets.

    :param radius: of the basic helix.
    :param pitch: of pitch of the helix per revolution.
    :param height: of the cyclinder containing the helix.
    :param cvrg_factor: if cvrg_factor is 0 no tapering occurs otherwise
        cvrg_factor is the "percentage" of the range
        of t where tapering occurs at the begining and end of
        that last_t - first_t rang. A ValueError exception is
        raised if first_t < 0 or > 0.5.
    :param inset_offset: the helix will start at z = inset_offset and will end
        at z = height - (2 * inset_offset).
    :param horz_offset: is added to the radius of the helix.
    :param vert_offset: is added to the nonimal z location of the helix
    :param first_t: is the first t value passed to the returned function
    :param last_t: is the last t value passed to the returned function

    Credit: Adam Urbanczyk from cadquery forum post:
        https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ
    """
    if cvrg_factor < 0 or cvrg_factor > 0.5:
        raise ValueError("cvrg_factor={cvrg_factor} should be 0 .. 0.5 inclusive")

    # Reduce the height by 2 * inset_offset. Threads start at inset_offset
    # and end at height - inset_offset
    helix_height: float = (height - (2 * inset_offset))

    # The number or revolutions of the helix within the helix_height
    # set to 1 if pitch or helix_height is 0
    turns: float = pitch / helix_height if pitch != 0 and helix_height != 0 else 1

    t_range: float = last_t - first_t

    taper_range: float = t_range * cvrg_factor

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
        rel_t: float = to / t_range if t_range != 0 else 0

        if (taper_range > 0) and (t < taper_out):
            # Taper out from point.
            # taper_scale is between 0 and 1
            taper_angle = pi / 2 * (t - first_t) / taper_range
        elif (taper_range == 0) or ((t >= taper_out) and (t < taper_in)):
            # No tapering, taper_scale = 1
            taper_angle = pi / 2
        else:
            # Taper in to a point.
            # taper_scale is between 1 and 0
            taper_angle = pi / 2 * (last_t - t) / taper_range

        taper_scale = sin(taper_angle)

        r: float = radius + (horz_offset * taper_scale)
        a: float = (2 * pi / turns) * rel_t

        x = r * sin(-a)
        y = r * cos(a)
        z = (
            (helix_height * (rel_t if pitch != 0 else 1))
            + (vert_offset * taper_scale)
            + inset_offset
        )

        result = (x, y, z)
        # print(f"f: ft={first_t} lt={last_t} rt={rel_t} tr={t_range")
        # print(f"f: tpr={taper_range} tpim={taper_in}") tpom={taper_out}")
        # print(f"f: tpa={taper_angle} tps={taper_scale} r={r} a={a}")
        # print(f"f: t={t} to={to} result={result}")
        return result

    return func
