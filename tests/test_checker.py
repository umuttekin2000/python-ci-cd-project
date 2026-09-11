import pytest
import requests
from pytest_mock import MockerFixture

from simple_http_checker.checker import check_urls


def test_check_urls_success(mocker: MockerFixture):
    # Mock the requests.get method to simulate a successful response
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True
    mocker_requests_get.return_value = mock_response

    urls = ["http://example.com"]
    results = check_urls(urls)

    mocker_requests_get.assert_called_once_with("http://example.com", timeout=5)

    assert results == {"http://example.com": "200 OK"}


def test_check_urls_client_error(mocker: MockerFixture):
    # Mock the requests.get method to simulate a connection error
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_response.ok = False
    mocker_requests_get.return_value = mock_response

    urls = ["http://example.com/nonexistent"]
    results = check_urls(urls)

    mocker_requests_get.assert_called_once_with(
        "http://example.com/nonexistent", timeout=5
    )

    assert results == {"http://example.com/nonexistent": "404 Not Found"}


@pytest.mark.parametrize(
    "error_exception, expected_status",
    [
        (requests.exceptions.Timeout, "Timeout"),
        (requests.exceptions.ConnectionError, "Connection Error"),
        (requests.exceptions.RequestException, "Request Error: RequestException"),
    ],
)
def test_check_urls_request_exception(
    mocker: MockerFixture,
    error_exception: type[requests.RequestException],
    expected_status: str,
):
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")
    mocker_requests_get.side_effect = error_exception(
        f"Simulated {expected_status} for testing"
    )

    urls = ["http://problem.com"]
    results = check_urls(urls)

    mocker_requests_get.assert_called_once_with("http://problem.com", timeout=5)

    assert results == {"http://problem.com": f"{expected_status}"}
    assert results[urls[0]] == expected_status


def test_check_urls_multiple_urls(mocker: MockerFixture):
    # Mock the requests.get method to simulate different responses for multiple URLs
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    def side_effect(url: str, timeout: int):
        mock_response = mocker.MagicMock(spec=requests.Response)
        if url == "http://example.com":
            mock_response.status_code = 200
            mock_response.reason = "OK"
            mock_response.ok = True
        elif url == "http://example.com/timeout":
            raise requests.exceptions.Timeout("Simulated timeout for testing")
        elif url == "http://example.com/error":
            raise requests.exceptions.ConnectionError(
                "Simulated connection error for testing"
            )
        return mock_response

    mocker_requests_get.side_effect = side_effect

    urls = [
        "http://example.com",
        "http://example.com/timeout",
        "http://example.com/error",
    ]
    results = check_urls(urls)

    assert results == {
        "http://example.com": "200 OK",
        "http://example.com/timeout": "Timeout",
        "http://example.com/error": "Connection Error",
    }


def test_check_urls_empty_list():
    urls: list[str] = []
    results = check_urls(urls)
    assert results == {}


def test_check_urls_custom_timeout(mocker: MockerFixture):
    # Mock the requests.get method to simulate a successful response
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True
    mocker_requests_get.return_value = mock_response

    urls = ["http://example.com"]
    custom_timeout = 10
    results = check_urls(urls, timeout=custom_timeout)

    mocker_requests_get.assert_called_once_with(
        "http://example.com", timeout=custom_timeout
    )

    assert results == {"http://example.com": "200 OK"}
