from click.testing import CliRunner
from src.cli import main

def test_search_not_configured():
    runner = CliRunner()
    result = runner.invoke(main, ["search", "test"])
    assert "Not configured" in result.output
    assert result.exit_code != 0
