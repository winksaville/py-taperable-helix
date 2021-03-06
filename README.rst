===============
Taperable Helix
===============

..
  TODO: eventually we'll enable the badges
  .. image:: https://img.shields.io/travis/winksaville/taperable_helix.svg
          :target: https://travis-ci.com/winksaville/taperable_helix

.. image:: https://img.shields.io/pypi/v/taperable_helix.svg
   :target: https://pypi.python.org/pypi/taperable_helix

.. image:: https://readthedocs.org/projects/taperable-helix/badge/?version=latest
    :target: https://taperable-helix.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Generate helixes that can optionally taper to a point at each end.

* GitHub repo: https://github.com/winksaville/py-taperable-helix/
* Documentation: https://taperable-helix.readthedocs.io/
* PyPi package: https://pypi.org/project/taperable-helix/
* Test PyPi package: https://test.pypi.org/project/taperable-helix/
* Free software: MIT license
* Source: `helix.py`_


Examples
--------

* `helical_line.py`_

.. code-block:: python

    def helical_line(
        radius: float = 5, pitch: float = 2, height: float = 6, num_points: int = 100
    ) -> List[Tuple[float, float, float]]:
        h: Helix = Helix(radius=radius, pitch=pitch, height=height)
        f = h.helix()
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
        fU = h.helix(HelixLocation(vert_offset=tri_height / 2))
        points_fU = list(map(fU, linspace(h.first_t, h.last_t, num=100, dtype=float)))

        # The Lower points, again horz_offset defaults to 0
        fL = h.helix(HelixLocation(vert_offset=-tri_height / 2))
        points_fL = list(map(fL, linspace(h.first_t, h.last_t, num=100, dtype=float)))

        # The Middle point, change vert_offset to 0
        fM = h.helix(HelixLocation(horz_offset=tri_width))
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

See `dev-requirements.in`_ for most up to date list:

* pip-tools
* bump2version
* wheel
* isort
* black
* flake8
* tox
* tox-conda
* coverage
* Sphinx~=3.2
* sphinx-autodoc-typehints~=1.11
* sphinx-prompt~=1.3
* sphinx_substitution_extensions>=2020.09.30, <2021.12.00
* twine
* pytest
* pytest-runner

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
.. _`dev-requirements.in`: https://github.com/winksaville/py-taperable-helix/blob/master/dev-requirements.in
