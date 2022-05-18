from datetime import datetime, date


def date_from_str(date_string: str) -> date:
    return datetime.strptime(date_string, '%Y-%m-%d').date()
