from __future__ import annotations

import subprocess
import typer
import uvicorn
cli = typer.Typer()


@cli.command("runserver")
def run_server(
    port: int = 8000,
    host: str = "localhost",
    log_level: str = "debug",
    reload: bool = True,
):
    """Run the API development server (uvicorn)."""
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@cli.command("format")
def format_code():
    """Format the code using ruff."""
    try:
        subprocess.run(["ruff", "format", "app", "lib", "validation"], check=True)
    except subprocess.CalledProcessError:
        typer.echo("Please fix the errors before committing.")
    finally:
        subprocess.run(["ruff", "clean"], check=True)

@cli.command("check")
def check_code():
    """Check the code using ruff."""
    try:
        subprocess.run(["ruff", "check", "app", "lib", "validation"], check=True)
    except subprocess.CalledProcessError:
        typer.echo("Please fix the errors before committing.")
    finally:
        subprocess.run(["ruff", "clean"], check=True)

if __name__ == "__main__":
    cli()
