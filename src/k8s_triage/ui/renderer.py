from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

def render_rca(markdown_content: str) -> None:
    """Render the final Root Cause Analysis report as formatted Markdown."""
    md = Markdown(markdown_content)
    panel = Panel(md, title="[bold blue]Kubernetes Triage Report[/bold blue]", border_style="blue")
    console.print()
    console.print(panel)
    console.print()
