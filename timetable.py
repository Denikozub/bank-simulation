from datetime import datetime, time, timedelta
from typing import Optional


class Timetable:
    def __init__(self, week_working_hours: list[tuple[Optional[time], Optional[time]]],
                 lunch_start: time, lunch_end: time):
        if len(week_working_hours) != 7:
            raise ValueError('Timetable should be set for 7 days!')
        for start, end in week_working_hours:
            if start is not None and start >= end:
                raise ValueError('Day should start before ending!')
        self._week_working_hours = week_working_hours.copy()
        self._lunch_start = lunch_start
        self._lunch_end = lunch_end

    def is_lunch(self, current_time: datetime) -> bool:
        return self._lunch_start < current_time.time() < self._lunch_end

    def is_working(self, current_time: datetime) -> bool:
        weekday = current_time.weekday()
        day_start, day_end = self._week_working_hours[weekday]
        return day_start is not None and day_start < current_time.time() < day_end and not self.is_lunch(current_time)

    def get_next_day_start(self, current_time: datetime) -> datetime:
        if self.is_working(current_time):
            return current_time
        weekday = (current_time.weekday() + 1) % 7
        date = current_time.date() + timedelta(days=1)
        while self._week_working_hours[weekday][0] is None:
            weekday = (weekday + 1) % 7
            date += timedelta(days=1)
        return datetime.combine(date, self._week_working_hours[weekday][0])
