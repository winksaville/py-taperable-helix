# from: https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ
from math import cos, degrees, pi, sin
from typing import Callable, Tuple


def converging_helix(
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
    Returns a function which can be used to create helixes that are
    as simple as a single line or be multiple helixes that start at
    a point then smoothly expand to the solid and then smoothly
    converge back to a point.

    The initial use case is to create triangular or trapazoidal threads
    for nuts and bolts. Invoking converging_helix multiple times with the
    same radius, pitch, inset_offset, first_t, and last_t but with differing values
    for cvrg_factor, horz_offset and vert_offset the final solid will start
    at a point expand to the desired shape and then converge back to a
    point.

    The helix is centered around the origin and radius and height define
    basic box of the helix, but inset_offset, cvrg_factor, horz_offset and
    vert_offset will modify the box. The parameters first_t and last_t
    define the range of the parameter "t" parameter to the returned
    function. The default values of first_t and last_t are 0 and 1. And
    t / (last_t - first_t) defines the relative t and if the difference
    is 0 the relative t will be 0 and only a single point will be created
    typically at the origin + any _offsets.

    :param radius: of the basic helix.
    :param pitch: of pitch of the helix per revolution.
    :param height: of the cyclinder containing the helix.
    :param cvrg_factor: if cvrg_factor is 0 no fading occurs
    ortherise cvrg_factor is the percentage of the range of t that fades occur
    at the begining and end of that range.
    :param inset_offset: the top and bottom of the helicial
    cyclinder where the helix actually starts.
    :param horz_offset: is added to the radius of the helix
    :param vert_offset: is added to the nonimal z location of the helix
    :param first_t: is the first t value passed to the returned function
    :param last_t: is the last t value passed to the returned function

    """
    # TODO: Test negative inset_offset works
    # if inset_offset < 0:
    #     raise ValueError("inset_offset must be >= 0")

    # Reduce the height by 2 * inset_offset. Threads start at inset_offset
    # and end at height - inset_offset
    helix_height: float = (height - (2 * inset_offset))

    # The number or revolutions of the helix within the helix_height
    turns: float = pitch / helix_height if pitch != 0 and helix_height != 0 else 1

    t_range: float = last_t - first_t

    # TODO: Test what happens with cvrg_factor > 0.5
    if cvrg_factor > 0.5:
        raise ValueError("cvrg_factor={cvrg_factor} > 0.5, should 0 .. 0.5 inclusive")

    # TODO: Test what happens with cvrg_factor < 0
    fade_range: float = t_range * cvrg_factor
    # fade_range: float = 0
    # if cvrg_factor > 0:
    #     fade_range = (last_t - first_t) * cvrg_factor

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
        rel_t: float = to / t_range if t_range != 0 else 0

        if (fade_range > 0) and (t < fade_in_mark):
            # FadeIn, fade_angle is 0 to 90deg so fade_scale is between 0 and 1
            fade_angle = +(pi / 2 * (t - first_t) / fade_range)
        elif (fade_range == 0) or ((t >= fade_in_mark) and (t < fade_out_mark)):
            # No fading set fade_angle to 90deg so sin(fade_angle) == 1
            fade_angle = pi / 2
        else:
            # FadeOut, fade_angle is 90 to 0deg so fade_scale is between 1 and 0
            fade_angle = -((2 * pi) - (pi / 2 * (last_t - t) / fade_range))
        fade_scale: float = sin(fade_angle)

        r: float = radius + (horz_offset * fade_scale)
        a: float = (2 * pi / turns) * rel_t

        x = r * sin(-a)
        y = r * cos(a)
        z = (
            (helix_height * (rel_t if pitch != 0 else 1))
            + (vert_offset * fade_scale)
            + inset_offset
        )

        result = (x, y, z)
        # print(f"f: first_t={first_t} last_t={last_t} to={to} rel_t={rel_t} tr={t_range} fr={fade_range} fim={fade_in_mark} fom={fade_out_mark} fa={fade_angle} fs={fade_scale} r={r} a={a}")
        # print(f"f: result={result}")
        return result

    return func
