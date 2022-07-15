"""
Odonto utilities
"""
import datetime



def get_current_financial_year():
    today = datetime.date.today()
    if today.month > 3:
        return (
            datetime.date(today.year, 4, 1),
            today
        )
    return (
        datetime.date(today.year-1, 4, 1),
        today
    )
