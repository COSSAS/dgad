from click.testing import CliRunner

from dgad.cli import cli


def test_cli():
    runner = CliRunner()
    test_args = [
        ["client", "--help"],
        ["client", "--domain", "wikipedia.org"],
        ["client", "-d", "wikipedia.org", "-d", "ajksdfhlkdjsfh.net"],
        ["client", "-fmt", "csv", "-f", "tests/data/domains_todo.csv"],
        ["client", "-n", "81", "-d", "ajksdfhlkdjsfh.net"],
        ["client", "-n", "52", "-fmt", "csv", "-f", "tests/data/domains_todo.csv"],
    ]
    for args in test_args:
        result = runner.invoke(cli, args)
        assert result.exit_code == 0
