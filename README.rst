================
taperable_helix
================

..
  TODO: eventually we'll enable the badges
  .. image:: https://img.shields.io/pypi/v/taperable_helix.svg
        :target: https://pypi.python.org/pypi/taperable_helix

  .. image:: https://img.shields.io/travis/winksaville/taperable_helix.svg
          :target: https://travis-ci.com/winksaville/taperable_helix

  .. image:: https://readthedocs.org/projects/taperable-helix/badge/?version=latest
         :target: https://taperable-helix.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status

Generate helexes that can taper to a point at each end.

* `helix.py`_

..
  # TODO: include the taperable_helix doc string here
  .. automodule:: taperable_helix.helix
     :members:
     :undoc-members:
     :show-inheritance:

Examples
--------

* `Helical line`_

.. image:: /data/helical_line.webp


* `Helical triangle`_

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
