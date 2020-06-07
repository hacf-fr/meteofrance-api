# Contribuer | Contributing

You will find instructions in English [here](#contributing).

Vous trouverez les instructions en français [ici](#contribuer).

## Contribuer

Vous êtes tous invités à contribuer à ce projet pour le maintenir ou l'améliorer.
Même si vous n'êtes pas un développeur, vous pouvez suremnent donner un coup de
main à la documentation.

### Préparer votre Pull Request (PR)

-   Commencez par faire un `fork` de ce dépot.
-   Clonez votre dépot sur votre machine de developpement.
-   Choisissez et installez votre environement de developpement (environement
    virtuel, container, etc...).
-   Installez le package python en mode edition avec ses prérequis de test:
    `pip install -e .[testing]`.
-   Créez une branche pour votre contribution.
-   Testez vos modifications avec la commande `pytest`.
-   Créez et envoyez la PR quand elle est prête.
-   Attendez les commentaires des relecteurs, répondez à leur questions ou demandes
    de mise au point.
-   Votre contribution est fusionnée dans le projet. Merci.

### Bonnes pratiques

Pour faciliter la maintenance et la relecture il est fortement recommandé
d'utiliser des outils pour s'assurer de la qualité du code et de son formatage.
Avec les librairies installées par la comande `pip install -e .[testing]`, vous
pouvez utiliser les commandes:

-   `pytest --cov` pour vérifer que les tests couvrent bien tout le code du
    package.
-   `flake8` pour vérfier que les bonnes pratiques Python sont respectées.
-   `pydocstyle` pour vérifier que les bonnes pratique des docstrings sont
    respectées.

Vous pouvez utiliser les lignes de commandes ci-dessus ou paramétrer votre
environnement de developpement pour utiliser ces outils ou similaires.

### Proposer une nouvelle fonctionnalité

Pour proposer vos idées d'amélioration, ouvrez une `issue` en utilisant le
modèle `feature request`.

## Contributing

You are all invited to contribute to this project for maintenance or improvement.
Even if you are not a developer, you can probably help to improve the documentation.

### Prepare your Pull Request (PR)

-   Start by forking this repository.
-   Clone this repository on your development machine.
-   Choose and setup your development environement (virtual environement, container,
    etc.).
-   Install the python package in edition mode with the test prerequisits:
    `pip install -e .[testing]`.
-   Create a branch for your contribution.
-   Test your change using the `pytest` command.
-   Create and send your PR when ready.
-   Wait for feedbacks from the reviewers, answer their questions or updates.
-   You contribution is merged in the project. Thank you.

### Guidelines

To make maintenance and review easier, we recommand you to use some tools ensuring
good code and format quality. With the librairies installed by
`pip install -e .[testing]` command, you can use the following commands:

-   `pytest --cov` to check code coevrage of the test suite.
-   `flake8` to check Python code best practices.
-   `pydocstyle` to check docstrings bespractices.

You can use those commands or setup your development environnement to use those
tools or silmilar ones.

### Feature suggestion

If you want to suggest a new feature for this project, please open an issue by
using the `feature request` template.
