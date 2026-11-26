import typer

from thoughtarchive.database import (
    initialise_database,
    add_thought,
    get_recent_thoughts,
    get_todays_thoughts,
)

from thoughtarchive.parser import (
    parse_add_args,
    parse_view_args,
)

from thoughtarchive.display import (
    display_thoughts,
)

app = typer.Typer(no_args_is_help=True)


def format_error(cmd: str, error) -> str:
    err_prefix = typer.style("ta error: ", fg=typer.colors.BRIGHT_BLACK)
    err_msg = typer.style(f"{error}", fg=typer.colors.RED, bold=True)
    err_help = typer.style(f"type `ta {cmd} --help` for more", fg=typer.colors.BRIGHT_BLACK)

    return err_prefix + err_msg + "\n" + err_help


@app.callback()
def main():
    initialise_database()


@app.command(
    help="the thought you want to save, followed by an optional date DD-MM(- YY or YYYY) and/or 24-hr time HH:MM",
    epilog="""
examples:
  ta add hello from me                  (now)
  ta add hello from me 11-11            (saved for 11th Nov 2026)
  ta add hello from me 12:34            (saved for today at 12:34)
  ta add "hello it's me" 11-11-11 11:11 (use quotes for special chars, or escape using backslash)
""",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }
)
def add(ctx: typer.Context):
    try:
        content, thought_date, thought_time = (
            parse_add_args(ctx.args)
        )

    except ValueError as error:
        typer.echo(format_error("add", error), err=True)
        raise typer.Exit(code=1)

    add_thought(
        content,
        thought_date,
        thought_time,
    )

    typer.echo(
        typer.style('thought "', fg=typer.colors.CYAN)
        + typer.style(content, fg=typer.colors.YELLOW)
        + typer.style('" saved!', fg=typer.colors.CYAN)
    )


@app.command(
    help="the number of recent thoughts you want to view (displayed oldest to newest)",
    epilog="""
    examples:
        ta view         (most recent 20)
        ta view 50      (most recent 50)
""",
    context_settings={
            "allow_extra_args": True,
            "ignore_unknown_options": True,
    }
)
def view(ctx: typer.Context):
    try:
        number = parse_view_args(ctx.args)

    except ValueError as error:
        typer.echo(format_error("view", error), err=True)
        raise typer.Exit(code=1)

    thoughts = get_recent_thoughts(number)

    if not thoughts:
        typer.secho("no thoughts found...", fg=typer.colors.BRIGHT_BLACK)
        return

    display_thoughts(thoughts)


@app.command(
    help="view your thoughts for this archive day."
)
def ls():
    try:
        thoughts = get_todays_thoughts()
    except Exception as error:
        typer.echo(format_error("ls", error), err=True)
        raise typer.Exit(code=1)

    if not thoughts:
        typer.echo("no thoughts recorded for this archive day...")
        raise typer.Exit()

    display_thoughts(thoughts)


if __name__ == "__main__":
    app()
