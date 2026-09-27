from typer.testing import CliRunner

from k8s_triage import __version__
from k8s_triage.cli import app

runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"k8s-triage version {__version__}" in result.stdout


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Kubernetes Triage Assistant CLI" in result.stdout
    assert "analyze" in result.stdout
    assert "interactive" in result.stdout
