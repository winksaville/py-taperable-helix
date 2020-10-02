===============
Taperable Helix
===============

..
  TODO: eventually we'll enable the badges
  .. image:: https://img.shields.io/pypi/v/taperable_helix.svg
        :target: https://pypi.python.org/pypi/taperable_helix

  .. image:: https://img.shields.io/travis/winksaville/taperable_helix.svg
          :target: https://travis-ci.com/winksaville/taperable_helix

.. image:: https://readthedocs.org/projects/taperable-helix/badge/?version=latest
         :target: https://taperable-helix.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status

Generate helixes that can optionally taper to a point at each end.

* GitHub repo: https://github.com/winksaville/py-taperable-helix/
* Documentation: https://taperable-helix.readthedocs.io/
* PyPi package: https://pypi.org/project/taperable-helix/
* Test PyPi package: https://test.pypi.org/project/taperable-helix/
* Free software: MIT license


Package Docs
------------

* docs: https://taperable-helix.readthedocs.io/en/latest/taperable_helix.html
* source: `helix.py`_

..
    I wish the code-block's below could be a `.. literalinclude::`,
    but I couldn't get that to work.

.. code-block:: python

    @dataclass
    class Helix:
        radius: float #: radius of the basic helix.
        pitch: float #: pitch of the helix per revolution. I.e the distance between the height of a single "turn" of the helix.
        height: float #: height of the cyclinder containing the helix.
        taper_out_rpos: float = 0 #: taper_out_rpos: is a decimal number with an inclusive range of 0..1 such that (taper_out_rpos * t_range) defines the t value where tapering out ends, it begins at t == first_t.  A ValueError exception is raised if taper_out_rpos < 0 or > 1 or taper_out_rpos > taper_in_rpos. Default is 0 which is no out taper
        taper_in_rpos: float = 1 #: taper_in_rpos: is a decimal number with an inclusive range of 0..1 such that (taper_in_rpos * t_range) defines the t value where tapering in begins, it ends at t == last_t.  A ValueError exception is raised if taper_out_rpos < 0 or > 1 or taper_out_rpos > taper_in_rpos. Default is 1 which is no in taper.
        inset_offset: float = 0 #: inset_offset: the helix will start at z = inset_offset and will end at z = height - (2 * inset_offset). Default 0.
        first_t: float = 0 #: first_t is the first t value passed to the returned function. Default 0
        last_t: float = 1 #: last_t is the last t value passed to the returned function. Default 1

    @dataclass
    class HelixLocation:
        radius: Optional[float] = None  #: radis of helix if none h.radius is used
        horz_offset: float = 0  #: horzitional offset added to the radius
        vert_offset: float = 0  #: vertical added to z of radius


    def helix(
        h: Helix, hl: Optional[HelixLocation] = None
    ) -> Callable[[float], Tuple[float, float, float]]:
        ...

Examples
--------

* `helical_line.py`_

.. code-block:: python

    def helical_line(
        radius: float = 5, pitch: float = 2, height: float = 6, num_points: int = 100
    ) -> List[Tuple[float, float, float]]:
        h: Helix = Helix(radius=radius, pitch=pitch, height=height)
        f = helix(h)
        points = list(map(f, linspace(start=0, stop=1, num=num_points, dtype=float)))
        # print(f"helical_line: points={points}")
        return points

    
.. image:: https://raw.githubusercontent.com/winksaville/py-taperable-helix/master/data/helical_line.webp


* `helical_tri.py`_

.. code-block:: python

    def helical_triangle(
        radius: float = 1,
        pitch: float = 2,
        height: float = 4,
        num_points: int = 100,
        tri_height: float = 0.2,
        tri_width: float = 0.2,
    ) -> Tuple[
        List[Tuple[float, float, float]],
        List[Tuple[float, float, float]],
        List[Tuple[float, float, float]],
    ]:

        # Create three helixes that taper to a point

        # Create the base Helix
        h: Helix = Helix(
            radius=radius, pitch=pitch, height=height, taper_out_rpos=0.1, taper_in_rpos=0.9
        )

        # The Upper points, horz_offset defaults to 0
        fU = helix(h, HelixLocation(vert_offset=tri_height / 2))
        points_fU = list(map(fU, linspace(h.first_t, h.last_t, num=100, dtype=float)))

        # The Lower points, again horz_offset defaults to 0
        fL = helix(h, HelixLocation(vert_offset=-tri_height / 2))
        points_fL = list(map(fL, linspace(h.first_t, h.last_t, num=100, dtype=float)))

        # The Middle point, change vert_offset to 0
        fM = helix(h, HelixLocation(horz_offset=tri_width))
        points_fM = list(map(fM, linspace(h.first_t, h.last_t, num=100, dtype=float)))

        return (points_fU, points_fM, points_fL)


.. image:: https://raw.githubusercontent.com/winksaville/py-taperable-helix/master/data/helical_tri.webp


Prerequisites
-------------

Using
#####

* python >= 3.7


Development and Examples
########################

* sphinx
* plotly

  * numpy
  * panda
  * python-kaleido

Credits
-------

This code originated from a post_ by Adam Urbanczyk to the CadQuery_ forum_ and this
package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _post: https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ
.. _CadQuery: https://github.com/cadquery/cadquery
.. _forum: https://groups.google.com/g/cadquery
.. _`helix.py`: https://github.com/winksaville/py-taperable-helix/blob/master/taperable_helix/helix.py
.. _`helical_line.py`: https://github.com/winksaville/py-taperable-helix/blob/master/examples/helical_line.py
.. _`helical_tri.py`: https://github.com/winksaville/py-taperable-helix/blob/master/examples/helical_tri.py
