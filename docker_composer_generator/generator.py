"""Script to generate a docker compose file with several clients."""

import logging
from pathlib import Path

import jinja2
import typer

from utils import config_logging, get_logger

logger = get_logger(__name__)
app = typer.Typer()

DEFAULT_PATH = Path(__name__).parent / "docker-compose-dev.yaml"


@app.command()
def main(nclients: int = 2, output: Path = DEFAULT_PATH):
    """Generate docker compose file"""
    config_logging(logging.INFO)

    env = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        loader=jinja2.FileSystemLoader(Path(__name__).parent),
    )
    template = env.get_template("docker-compose-template.j2")
    render = template.render(nclients=nclients)

    with open(output, "w") as f:  # pylint: disable=unspecified-encoding,invalid-name
        f.write(render)

    logger.info("Docker compose yaml file saved to %s", output)


if __name__ == "__main__":
    app()
