import logging
from collections.abc import (
    Collection,  # Collection is used to type hint the urls argument in the main function
)

import click

from simple_http_checker.checker import check_urls  # Adjust import path if needed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument("urls", nargs=-1)
@click.option("--timeout", default=5, help="Timeout for the HTTP request in seconds.")
@click.option(
    "-v", "--verbose", is_flag=True, help="Enable debug logging."
)  # Note '-v' instead of "v"
def main(urls: Collection[str], timeout: int, verbose: bool):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled. Debug logging is active.")

    if not urls:
        logger.error("No URLs provided. Please provide at least one URL to check.")
        click.echo("Error: No URLs provided. Please provide at least one URL to check.")
        return

    logger.info(
        f"Starting check for {len(urls)} URLs with a timeout of {timeout} seconds."
    )
    logger.info(f"Received urls: {urls}")
    logger.info(f"Received timeout: {timeout}")
    logger.info(f"Received verbose flag: {verbose}")

    if urls:
        results = check_urls(list(urls), timeout=timeout)
        for url, status in results.items():
            if "OK" in status:
                fg_color = "green"
            elif "Timeout" in status:
                fg_color = "yellow"
            else:
                fg_color = "red"
            click.echo(
                click.style(f"{url:<40} -> {status}", fg=fg_color)
            )  # Color the output based on status


if __name__ == "__main__":
    main()  # Default entry point for the CLI
