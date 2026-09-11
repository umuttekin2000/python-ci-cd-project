from click.testing import CliRunner
from pytest_mock import MockerFixture

from simple_http_checker.cli import main


def test_cli_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Error: No URLs provided" in result.output


def test_cli_single_url(mocker: MockerFixture):
    # Mock the check_urls function to return a predefined result
    mocker.patch(
        "simple_http_checker.cli.check_urls",
        return_value={"http://example.com": "200 OK"},
    )

    runner = CliRunner()
    result = runner.invoke(main, ["http://example.com"])

    assert result.exit_code == 0
    assert "http://example.com" in result.output
    assert "200 OK" in result.output
