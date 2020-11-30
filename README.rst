Météo-France Python API
=======================

Client Python pour l'API Météo-France. | Python client for Météo-France API.

|PyPI| |GitHub Release| |Python Version| |License|

|Read the Docs| |Tests| |Codecov| |GitHub Activity|

|pre-commit| |Black|


.. |PyPI| image:: https://img.shields.io/pypi/v/meteofrance-api
   :target: https://pypi.org/project/meteofrance-api/
   :alt: PyPI
.. |GitHub Release| image:: https://img.shields.io/github/release/hacf-fr/meteofrance-api.svg
   :target: https://github.com/hacf-fr/meteofrance-api/releases
   :alt: GitHub Release
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/meteofrance-api
   :target: https://pypi.org/project/meteofrance-api/
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/meteofrance-api
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/meteofrance-api/latest.svg?label=Read%20the%20Docs
   :target: https://meteofrance-api.readthedocs.io/
   :alt: Read the documentation at https://meteofrance-api.readthedocs.io/
.. |Tests| image:: https://github.com/hacf-fr/meteofrance-api/workflows/Tests/badge.svg
   :target: https://github.com/hacf-fr/meteofrance-api/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/hacf-fr/meteofrance-api/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hacf-fr/meteofrance-api
   :alt: Codecov
.. |GitHub Activity| image:: https://img.shields.io/github/commit-activity/y/hacf-fr/meteofrance-api.svg
   :target: https://github.com/hacf-fr/meteofrance-api/commits/master
   :alt: GitHub Activity
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

You will find English README content in the section `For English speaking users`_.

Vous trouverez le contenu francophone du README dans la section `Pour les francophones`_.

Pour les francophones
---------------------

Description
^^^^^^^^^^^

Ce package Python permet de gérer la communication avec l'API non publique de
Météo-France utilisée par les applications mobiles officielles.

Le client permet:

* Rechercher des lieux de prévisions.
* Accéder aux prévisions météorologiques horaires ou quotidiennes.
* Accéder aux prévisions de pluie dans l'heure quand disponibles.
* Accéder aux alertes météo pour chaque département français et d'Andorre. Deux
  bulletins sont disponibles : un synthétique et un second avec l'évolution des alertes
  pour les prochaines 24 heures (exemple `ici <https://vigilance.meteofrance.fr/fr/gers>`_).

Ce package a été développé avec l'intention d'être utilisé par `Home-Assistant <https://home-assistant.io/>`_
mais il peut être utilisé dans d'autres contextes.

Installation
^^^^^^^^^^^^

Pour utiliser le module Python ``meteofrance`` vous devez en premier installer
le package en utilisant pip_ depuis PyPI_:

.. code:: console

   $ pip install meteofrance-api


Vous pouvez trouver un exemple d'usage dans un module Python en regardant
`le test d'intégration <tests/test_integrations.py>`_.

Contribuer
^^^^^^^^^^

Les contributions sont les bienvenues. Veuillez consulter les bonnes pratiques
détaillées dans `CONTRIBUTING.rst`_.


For English speaking users
--------------------------

Description
^^^^^^^^^^^^

This Python package manages the communication with the private Météo-France API
used by the official mobile applications.

The client allows:

* Search a forecast location.
* Fetch daily or hourly weather forecast.
* Fetch rain forecast within the next hour if available.
* Fetch the weather alerts or phenomenoms for each French department or Andorre.
  Two bulletin are availabe: one basic and an other advanced with the timelaps evolution
  for the next 24 hours (example `here <https://vigilance.meteofrance.fr/fr/gers>`_).

This package have been developed to be used with `Home-Assistant <https://home-assistant.io/>`_
but it can be used in other contexts.

Installation
^^^^^^^^^^^^

To use the ``meteofrance`` Python module, you have to install this package first via
pip_ from PyPI_:

.. code:: console

   $ pip install meteofrance-api

You will find an example ot usage in a Python program in the `integration test <tests/test_integrations.py>`_.

Contributing
^^^^^^^^^^^^

Contributions are welcomed. Please check the guidelines in `CONTRIBUTING.rst`_.

Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _pip: https://pip.pypa.io/

.. github-only
.. _CONTRIBUTING.rst: CONTRIBUTING.rst
