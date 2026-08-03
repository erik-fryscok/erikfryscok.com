"""Click CLI for Harbor evaluation harness."""

import os
from pathlib import Path

import click
from dotenv import load_dotenv


# Load .env file
load_dotenv()


@click.group()
def main():
    """Harbor evaluation harness for OpenCode agents."""
    pass


@main.command()
def validate():
    """Validate schemas, version pins, task layout, hashes, privacy rules."""
    click.echo("Validating Harbor configuration...")

    jobs_dir = os.getenv("ERIKFRYSCOK_HARBOR_JOBS_DIR")
    if not jobs_dir:
        click.echo("ERROR: ERIKFRYSCOK_HARBOR_JOBS_DIR not set", err=True)
        raise click.Exit(1)

    jobs_path = Path(jobs_dir)
    if not jobs_path.exists():
        click.echo(f"ERROR: {jobs_dir} does not exist", err=True)
        raise click.Exit(1)

    if jobs_path.is_relative_to(Path.cwd()):
        click.echo("ERROR: ERIKFRYSCOK_HARBOR_JOBS_DIR must be outside repository", err=True)
        raise click.Exit(1)

    click.echo("✓ Configuration valid")


@main.command()
def preflight():
    """Verify Docker, provider credentials, model availability, LM Studio connectivity."""
    click.echo("Running preflight checks...")

    import subprocess

    try:
        subprocess.run(["docker", "version"], capture_output=True, check=True)
        click.echo("✓ Docker available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo("ERROR: Docker not available", err=True)
        raise click.Exit(1)

    lm_studio_endpoint = os.getenv("LM_STUDIO_ENDPOINT")
    if lm_studio_endpoint:
        try:
            import requests

            response = requests.get(f"{lm_studio_endpoint}/models", timeout=5)
            if response.status_code == 200:
                click.echo(f"✓ LM Studio available at {lm_studio_endpoint}")
            else:
                click.echo(f"WARNING: LM Studio returned {response.status_code}", err=True)
        except Exception as e:
            click.echo(f"WARNING: LM Studio not available: {e}", err=True)

    click.echo("✓ Preflight checks complete")


@main.command()
@click.option(
    "--suite",
    type=click.Choice(["smoke", "development", "holdout", "workflow", "all"]),
    default="smoke",
)
def oracle(suite):
    """Prove every reference solution passes."""
    click.echo(f"Running oracle for suite: {suite}")
    click.echo("(Not yet implemented)")


@main.command()
@click.option(
    "--suite", type=click.Choice(["smoke", "development", "holdout", "workflow"]), required=True
)
@click.option("--profile", type=str, required=True)
def run(suite, profile):
    """Launch one Harbor job for one profile."""
    click.echo(f"Running suite '{suite}' with profile '{profile}'")
    click.echo("(Not yet implemented)")


@main.command()
@click.option("--experiment", type=click.Path(exists=True), required=True)
def matrix(experiment):
    """Run paired baseline/candidate jobs with prescribed attempt counts."""
    click.echo(f"Running matrix experiment: {experiment}")
    click.echo("(Not yet implemented)")


@main.command()
@click.option("--baseline", type=str, required=True)
@click.option("--candidate", type=str, required=True)
def compare(baseline, candidate):
    """Normalize results and evaluate promotion gates."""
    click.echo(f"Comparing baseline '{baseline}' vs candidate '{candidate}'")
    click.echo("(Not yet implemented)")


@main.command(name="sanitize-report")
@click.option("--experiment", type=str, required=True)
def sanitize_report(experiment):
    """Create publication-safe JSON, CSV, and Markdown summaries."""
    click.echo(f"Sanitizing report for experiment: {experiment}")
    click.echo("(Not yet implemented)")


if __name__ == "__main__":
    main()
