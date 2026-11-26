import typer

from thoughtarchive.database import (
    initialise_database,
    add_thought,
)

from thoughtarchive.parser import (
    parse_add_arguments,
)

app = typer.Typer(no_args_is_help=True)


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
            parse_add_arguments(ctx.args)
        )

    except ValueError as error:
        err_prefix = typer.style("ta error: ", fg=typer.colors.BRIGHT_BLACK)
        err_msg = typer.style(f"{error}", fg=typer.colors.RED, bold=True)
        err_help = typer.style(f"type `ta add --help` for more", fg=typer.colors.BRIGHT_BLACK)

        typer.echo(err_prefix + err_msg + "\n" + err_help, err=True)
        raise typer.Exit(code=1)

    add_thought(
        content,
        thought_date,
        thought_time,
    )

    typer.echo(f'thought "{content}" saved!')


if __name__ == "__main__":
    app()
