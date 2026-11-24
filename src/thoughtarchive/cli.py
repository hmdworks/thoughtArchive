from datetime import date, datetime, timedelta

import typer

from thoughtarchive.database import (
    initialise_database,
    add_thought,
)

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main():
    initialise_database()


def get_archive_datetime() -> tuple[str, str]:
    now = datetime.now().astimezone()

    archive_date = now.date()

    if now.hour < 5:
        archive_date -= timedelta(days=1)

    return archive_date.isoformat(), now.strftime("%H:%M")


def validate_date(value: str) -> str:
    parts = value.split("-")

    try:
        if len(parts) == 2:
            day, month = parts

            if len(day) != 2 or len(month) != 2:
                raise ValueError

            year = date.today().year

        elif len(parts) == 3:
            day, month, year = parts

            if (
                len(day) != 2
                or len(month) != 2
                or len(year) != 4
            ):
                raise ValueError

        else:
            raise ValueError

        parsed_date = date(
            int(year),
            int(month),
            int(day),
        )

    except ValueError:
        raise typer.BadParameter(
            f"use DD-MM or DD-MM-YYYY, e.g. 01-01 or 13-01-2025"
        )

    return parsed_date.isoformat()


def validate_time(value: str) -> str:
    try:
        parsed_time = datetime.strptime(value, "%H:%M")
    except ValueError:
        raise typer.BadParameter(
            "please use HH:MM format (24-hour time)"
        )

    if parsed_time.strftime("%H:%M") != value:
        raise typer.BadParameter(
            "please use HH:MM format (24-hour time)"
        )

    return value


@app.command()
def add(
    content: str = typer.Argument(
        ...,
        help="the thought you want to save (in quotes)",
    ),
    thought_date: str | None = typer.Argument(
        None,
        help="optional date (DD-MM or DD-MM-YYYY)",
    ),
    thought_time: str | None = typer.Argument(
        None,
        help="optional time (HH:MM)",
    ),
):

    current_date, current_time = get_archive_datetime()

    if thought_date is None:
        thought_date = current_date
        thought_time = thought_time or current_time
    else:
        thought_date = validate_date(thought_date)

    if thought_time is not None:
        thought_time = validate_time(thought_time)

    add_thought(
        content,
        thought_date,
        thought_time,
    )

    typer.echo(f'thought "{content}" saved!')


if __name__ == "__main__":
    app()
