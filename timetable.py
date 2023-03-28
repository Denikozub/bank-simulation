from typing import Optional
from datetime import datetime, time, timedelta


class Timetable:
    def __init__(self, week_working_hours: list[tuple[Optional[time], Optional[time]]],
                 lunch_start: time, lunch_end: time):
        if len(week_working_hours) != 7:
            raise ValueError('Timetable should be set for 7 days!')
        for start, end in week_working_hours:
            if start is not None and start >= end:
                raise ValueError('Day should start before ending!')
        self.__week_working_hours = week_working_hours.copy()
        self.__lunch_start = lunch_start
        self.__lunch_end = lunch_end

    def __is_lunch(self, current_time: datetime) -> bool:
        return self.__lunch_start < current_time.time() < self.__lunch_end

    def is_working(self, current_time: datetime) -> bool:
        weekday = current_time.weekday()
        day_start, day_end = self.__week_working_hours[weekday]
        return day_start < current_time.time() < day_end and not self.__is_lunch(current_time)

    def get_next_day_start(self, current_time: datetime) -> datetime:
        if self.is_working(current_time):
            return current_time
        if self.__is_lunch(current_time):
            return datetime.combine(current_time.date(), self.__lunch_end)
        weekday = (current_time.weekday() + 1) % 7
        date = current_time.date() + timedelta(days=1)
        while self.__week_working_hours[weekday][0] is None:
            weekday = (weekday + 1) % 7
            date += timedelta(days=1)
        return datetime.combine(date, self.__week_working_hours[weekday][0])
