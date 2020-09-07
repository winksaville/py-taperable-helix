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

Generate helixes that can taper to a point at each end.

* `helix.py`_

..
        I wish the code-block's below could be a `.. literalinclude::`,
        but I couldn't get that to work.

.. code-block:: python

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
            Returns a pure function. This returned function has one parameter,
            an inclusive value between first_t and last_t which represents the
            relative helix height. The returned value is the corresponding
            point on the helix and is returned as a tuple(x, y, z).

            A helix can be as simple as a single line or be a set of helical "wires"
            which define a "solid" that can start at a point and the smoothly expand
            to the desired "solid" and then smoothly taper back to a point.

            The nomial use case is to create triangular or trapazoidal threads
            for nuts and bolts. This is accomplished by invoking helix
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

            Credit: Adam Urbanczyk from cadquery forum post:
                https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ

            ...
            """

Examples
--------

* `Helical line`_

.. code-block:: python

        def helical_line(
            radius: float = 5, pitch: float = 2, height: float = 6, num_points: int = 100
        ) -> List[Tuple[float, float, float]]:
            f = helix(radius, pitch, height)
            points = list(map(f, linspace(start=0, stop=1, num=num_points, dtype=float)))
            # print(f"helical_line: points={points}")
            return points

    
.. image:: /data/helical_line.webp


* `Helical triangle`_

.. code-block:: python

        def helical_triangle(
            radius: float = 1,
            pitch: float = 2,
            height: float = 4,
            num_points: int = 100,
            tri_height=0.2,
            tri_width=0.2,
        ) -> (
            List[Tuple[float, float, float]],
            List[Tuple[float, float, float]],
            List[Tuple[float, float, float]],
        ):
            cvrg_factor = 0.1
            first_t = 0
            last_t = 1

            # Create three helixes that taper to a point
            fU = helix(
                radius, pitch, height, cvrg_factor=cvrg_factor, vert_offset=tri_height / 2
            )
            points_fU = list(map(fU, linspace(first_t, last_t, num=100, dtype=float)))

            fM = helix(radius, pitch, height, cvrg_factor=cvrg_factor, horz_offset=tri_width)
            points_fM = list(map(fM, linspace(first_t, last_t, num=100, dtype=float)))

            fL = helix(
                radius, pitch, height, cvrg_factor=cvrg_factor, vert_offset=-tri_height / 2
            )
            points_fL = list(map(fL, linspace(first_t, last_t, num=100, dtype=float)))
            return (points_fU, points_fM, points_fL)

.. image:: /data/helical_tri.webp


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
.. _`Helical Line`: /examples/helical_line.py
.. _`Helical triangle`: /examples/helical_tri.py
.. _`helix.py`: /taperable_helix/helix.py
