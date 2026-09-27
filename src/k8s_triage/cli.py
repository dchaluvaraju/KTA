
import typer
from rich.console import Console

from k8s_triage import __version__
from k8s_triage.agent.loop import AgentController
from k8s_triage.ui.renderer import render_rca

app = typer.Typer(help="Kubernetes Triage Assistant CLI")
console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"k8s-triage version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Kubernetes Triage Assistant CLI."""

@app.command()
def analyze(
    namespace: str = typer.Option(..., "--namespace", "-n", help="Namespace to analyze"),
    pod: str | None = typer.Option(None, "--pod", "-p", help="Specific pod to investigate"),
    prompt: str | None = typer.Option(None, "--prompt", help="Additional context or prompt")
) -> None:
    """Analyze a specific namespace or pod for issues."""
    try:
        agent = AgentController()
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        raise typer.Exit(1)
        
    query = f"Investigate issues in namespace '{namespace}'."
    if pod:
        query += f" Specifically look at pod '{pod}'."
    if prompt:
        query += f" Additional context from user: {prompt}"
        
    try:
        result = agent.run(query)
        render_rca(result)
    except Exception as e:
        console.print(f"[bold red]Analysis Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command()
def interactive() -> None:
    """Start an interactive triage session."""
    try:
        agent = AgentController()
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        raise typer.Exit(1)
        
    console.print("[bold green]Welcome to Kubernetes Triage Assistant Interactive Shell.[/bold green]")
    console.print("Type 'exit' or 'quit' to leave.")
    
    while True:
        try:
            user_input = console.input("\n[bold yellow]k8s-triage>[/bold yellow] ")
            if user_input.lower() in ["exit", "quit"]:
                break
            if not user_input.strip():
                continue
                
            result = agent.run(user_input)
            render_rca(result)
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    app()
