from datetime import date, datetime, timedelta
import re


def get_archive_datetime() -> tuple[str, str]:
    now = datetime.now().astimezone()

    archive_date = now.date()

    if now.hour < 5:
        archive_date -= timedelta(days=1)

    return archive_date, now.strftime("%H:%M")


def validate_date(value: str) -> date:
    parts = value.split("-")

    try:
        if len(parts) == 2:
            day, month = parts
            year = date.today().year

        elif len(parts) == 3:
            day, month, year = parts

            if len(year) == 2:
                year = f"20{year}"

            if len(year) != 4:
                raise ValueError

        else:
            raise ValueError

        if len(day) != 2 or len(month) != 2:
            raise ValueError

        return date(int(year), int(month), int(day))

    except ValueError:
        raise ValueError(
            "use valid dates as DD-MM, DD-MM-YY or DD-MM-YYYY"
        )


def validate_time(value: str) -> str:
    if not re.fullmatch(r"\d{2}:\d{2}", value):
        raise ValueError("use HH:MM format")

    try:
        datetime.strptime(value, "%H:%M")
    except ValueError:
        raise ValueError("invalid time, use 24hr")

    return value


def validate_not_future(
    thought_date: date,
    thought_time: str | None,
) -> None:
    now = datetime.now().astimezone()

    if thought_date > now.date():
        raise ValueError("thought date cannot be in the future")

    if thought_date == now.date() and thought_time is not None:
        selected_time = datetime.strptime(
            thought_time, "%H:%M"
        ).time()

        if selected_time > now.time().replace(tzinfo=None):
            raise ValueError("thought time cannot be in the future")


def parse_add_arguments(
    arguments: list[str],
) -> tuple[str, str, str | None]:

    content_parts = arguments.copy()
    datetime_args = []

    while content_parts:
        argument = content_parts[-1]

        if (
            re.fullmatch(
                r"\d{2}-\d{2}(?:-\d{2}|\-\d{4})?",
                argument,
            )
            or re.fullmatch(r"\d{1,2}:\d{2}", argument)
        ):
            datetime_args.insert(0, content_parts.pop())
        else:
            break

    content = " ".join(content_parts).strip()

    if not content:
        raise ValueError("thought content cannot be empty...")

    thought_date, thought_time = get_archive_datetime()

    date_given = False
    time_given = False

    for argument in datetime_args:

        if re.fullmatch(
            r"\d{2}-\d{2}(?:-\d{2}|\-\d{4})?",
            argument,
        ):
            if date_given:
                raise ValueError("only one date is allowed!")

            thought_date = validate_date(argument)
            date_given = True

        elif re.fullmatch(r"\d{1,2}:\d{2}", argument):
            if time_given:
                raise ValueError("only one time is allowed!")

            thought_time = validate_time(argument)
            time_given = True

    if date_given and not time_given:
        thought_time = None

    validate_not_future(thought_date, thought_time)

    return content, thought_date.isoformat(), thought_time
