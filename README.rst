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
        tri_height: float = 0.2,
        tri_width: float = 0.2,
    ) -> (
        List[Tuple[float, float, float]],
        List[Tuple[float, float, float]],
        List[Tuple[float, float, float]],
    ):
        taper_rpos = 0.1
        first_t = 0
        last_t = 1

        # Create three helixes that taper to a point
        fU = helix(radius, pitch, height, taper_rpos=taper_rpos, vert_offset=tri_height / 2)
        points_fU = list(map(fU, linspace(first_t, last_t, num=100, dtype=float)))

        fM = helix(radius, pitch, height, taper_rpos=taper_rpos, horz_offset=tri_width)
        points_fM = list(map(fM, linspace(first_t, last_t, num=100, dtype=float)))

        fL = helix(
            radius, pitch, height, taper_rpos=taper_rpos, vert_offset=-tri_height / 2
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
