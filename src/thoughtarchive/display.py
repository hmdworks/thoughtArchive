from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from rich.text import Text

console = Console()


def display_thoughts(thoughts):
    table = Table(title="thoughts from the Archive",
                style="dim bold",
                header_style="dim bold",
                show_edge=False
            )

    table.add_column("id", style="dim")
    table.add_column("date", style="dim")
    table.add_column("time", style="dim")
    table.add_column(style="cyan bold")

    for thought in thoughts:
        table.add_row(
            str(thought["id"]),
            thought["date"],
            thought["time"] or "—",
            thought["content"]
        )

    console.print(Padding(table, (1,0)), new_line_start=True)
