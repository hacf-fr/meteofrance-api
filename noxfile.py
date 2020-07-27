"""Nox sessions."""
import nox

locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.8", "3.7", "3.6"])
def tests(session):
    """Run the test suite."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.8", "3.7", "3.6"])
def lint(session):
    """Ling using flake8."""
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("flake8", *args)
