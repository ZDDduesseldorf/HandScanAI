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
    """Format the code using black and isort."""
    subprocess.run(["black", "."])
    subprocess.run(["isort", "."])


if __name__ == "__main__":
    run_server()
