import logging

import requests

logger = logging.getLogger(__name__)


def check_urls(urls: list[str], timeout: int = 5) -> dict[str, str]:
    """
    Check the status of a list of URLs.

    Args:
        urls (List[str]): A list of URLs to check.
        timeout (int): The timeout for the HTTP request in seconds.

    Returns:
        Dict[str, str]: A dictionary with URLs as keys and their status codes as values.
    """
    logger.info(f"Checking {len(urls)} URLs with a timeout of {timeout} seconds.")

    results: dict[str, str] = {}

    for url in urls:
        status: str = "Unknown"
        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)

            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "Timeout"
            logger.warning(f"Request to {url} timed out.")
        except requests.exceptions.ConnectionError:
            status = "Connection Error"
            logger.warning(f"Connection error occurred while checking {url}.")
        except requests.exceptions.RequestException as e:
            status = f"Request Error: {type(e).__name__}"
            logger.exception(f"An expected request error occurred while checking {url}")
        results[url] = status
        logger.debug(f"Checked URL: {url:<40} -> {status}")

    logger.info("URL checking completed.")
    return results
