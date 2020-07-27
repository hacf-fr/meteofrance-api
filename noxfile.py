"""Nox sessions."""
import nox


@nox.session(python=["3.8", "3.7", "3.6"])
def tests(session):
    """Run the test suite."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
