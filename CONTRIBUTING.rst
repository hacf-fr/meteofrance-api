Contribuer | Contributing
=========================

You will find instructions in English in the section `Contributing`_.

Vous trouverez les instructions en français dans la section `Contribuer`_.

Contribuer
----------

Vous êtes tous invités à contribuer à ce projet pour le maintenir ou l'améliorer.
Même si vous n'êtes pas un développeur, vous pouvez suremnent donner un coup de
main en remontant les bugs constatés, en partageant vos idées d'amélioration ou
en participant à la documentation.

Préparer votre environement de développement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vous aurez besoin de Python 3.6+ et des outils suivants:

- Poetry_
- Nox_

Installez le package avec les dépendances de développement:

.. code:: console

   $ poetry install

Vous pouvez maintenant utiliser une session interactive Python:

.. code:: console

   $ poetry run python

Je vous recommande d'installer un pre-commit-hook pour lancer automatiquement quelques
vérfication avant de commit vos modifications.

.. code:: console

   $ nox -s pre-commit -- install

Tester le projet
^^^^^^^^^^^^^^^^

Dérouler la suite de tests complète:

.. code:: console

   $ nox

Lister toutes les sessions disponibles dans Nox:

.. code:: console

   $ nox --list-sessions

Vous pouvez lancer une session Nox spécifique. Par exemple, lancez la suite de
tests unitaires avec:

.. code:: console

   $ nox --session=tests

Les tests unitaires sont dans le répertoire `tests` et utilisent le framework pytest.

Soumettre votre Pull Request (PR)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ouvrez une `pull request`_ pour proposer des changements à ce projet.

Votre pull request doit vérifier les conditions suivantes pour être acceptée:

* La suite de tests Nox doit réussir sans erreurs ni warning.
* Doit inclure des tests unitaires. Ce projet maintien une couverture de code à 100%.

Proposer une nouvelle fonctionnalité
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour proposer vos idées d'amélioration, ouvrez une `issue <https://github.com/hacf-fr/meteofrance-api/issues>`_
en utilisant le modèle ``feature request``.

Contributing
------------

You are all invited to contribute to this project for maintenance or improvement.
Even if you are not a developer, you can probably help to report some bugs, share
improvements ideas, or contribute to the documentation.

How to set up your development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need Python 3.6+ and the following tools:

- Poetry_
- Nox_

Install the package with development requirements:

.. code:: console

   $ poetry install

You can now run an interactive Python session, or the command-line interface:

.. code:: console

   $ poetry run python

I recommand to install a pre-commit-hook to have some checks done automatically before you commit your changes.

.. code:: console

   $ nox -s pre-commit -- install

How to test the project
^^^^^^^^^^^^^^^^^^^^^^^

Run the full test suite:

.. code:: console

   $ nox

List the available Nox sessions:

.. code:: console

   $ nox --list-sessions

You can also run a specific Nox session. For example, invoke the unit test suite like this:

.. code:: console

   $ nox --session=tests

Unit tests are located in the tests directory, and are written using the pytest testing framework.

How to submit changes
^^^^^^^^^^^^^^^^^^^^^

Open a `pull request`_ to submit
changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.

Feature suggestion
^^^^^^^^^^^^^^^^^^

If you want to suggest a new feature for this project, please open an `issue <https://github.com/hacf-fr/meteofrance-api/issues>`_
by using the `feature request` template.

.. _Poetry: https://python-poetry.org/
.. _Nox: https://nox.thea.codes/
.. _pull request: https://github.com/hacf-fr/meteofrance-api/pulls
