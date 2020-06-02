# meteofrance-api

Client Python pour l'API Météo-France. | Python client for Météo-France API.

[![Build Status][build-shield]][build]
[![codecov][codecov-shield]][codecov]
[![License][license-shield]](LICENSE)

[![GitHub Release][releases-shield]][releases]
[![PyPI version][pypi-shield]][pypi]
[![GitHub Activity][commits-shield]][commits]

You will find English README content [here](#for-english-speaking-users).

Vous trouverez le contenu francophone du README [ici](#pour-les-francophones).

## Pour les francophones

### Description

Ce pacakge Python permet de gérer la communication avec l'API non publique de
Météo-France utilisée par les applications moblies officielles.

Le client permet:

-   Rechercher des lieux de prévisions.
-   Accéder aux prévisions météorologiques horraires ou quotidiennes.
-   Accéder aux prévisions de pluie dans l'heure quand disponibles.
-   Accéder aux alertes météo pour chaque département français et l'Andorre. Deux
    bulletins sont disponibles : un synthétique et un second avec l'évolution des alertes
    pour les prochaines 24 heures (exemple [ici](http://vigilance.meteofrance.com/Bulletin_sans.html?a=dept32&b=2&c=)).

Ce package a été développé avec l'intention d'être utilisé par [Home-Assistant](https://home-assistant.io/) mais il peut être utilsé dans d'autres contextes.

### Installation

Pour utiliser le module Python `meteofrance` vous devez en premier installer
le package:

`pip install meteofrance-api`

Vous pouvez trouver un exemple d'usage dans un module Python en regardant [le test d'intégration](tests/test_integrations.py).

### Contribuer

Les contributions sont les bienvenues. Veuillez consulter les bonnes pratiques
détaillées dans [`CONTRIBUTING.md`](CONTRIBUTING.md).

## For English speaking users

### Descritption

This Python package manages the communication with the private Météo-France API
used by the official moblie applications.

The client allows:

-   Search a forecast location.
-   Fetch daily or hourly weather forecast.
-   Fetch rain forecast within the next hour if available.
-   Fetch the weather alerts or phenomenoms for each French department or Andorre.
    Two bulletin are availabe: one basic and an other advanced with the timelaps evolution for the next 24 hours (example [here](http://vigilance.meteofrance.com/Bulletin_sans.html?a=dept32&b=2&c=)).

This package have been developed to be used with [Home-Assistant](https://home-assistant.io/) but it can be used in other contexts.

### Installation

To use the `meteofrance` Python  module, you have to install this package first:

`pip install meteofrance-api`

You will find an example ot usage in a Python program in the [integration test](tests/test_integrations.py).

### Contributing

Contributions are welcomed. Please check the guidelines in [`CONTRIBUTING.md`](CONTRIBUTING.md).

[commits-shield]: https://img.shields.io/github/commit-activity/y/hacf-fr/meteofrance-api.svg?style=for-the-badge

[commits]: https://github.com/hacf-fr/meteofrance-api/commits/master

[license-shield]: https://img.shields.io/github/license/hacf-fr/meteofrance-api.svg?style=for-the-badge

[releases-shield]: https://img.shields.io/github/release/hacf-fr/meteofrance-api.svg?style=for-the-badge

[releases]: https://github.com/hacf-fr/meteofrance-api/releases

[build-shield]: https://img.shields.io/github/workflow/status/hacf-fr/meteofrance-api/Python%20package?style=for-the-badge

[build]: https://github.com/hacf-fr/meteofrance-api/actions?query=workflow%3A%22Python+package%22

[codecov-shield]: https://img.shields.io/codecov/c/github/hacf-fr/meteofrance-api?style=for-the-badge

[codecov]: https://codecov.io/gh/hacf-fr/meteofrance-api

[pypi-shield]: https://img.shields.io/pypi/v/meteofrance-api?style=for-the-badge

[pypi]: https://pypi.org/project/meteofrance-api/
