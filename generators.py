from typing import Optional
from datetime import timedelta, datetime
from numpy.random import normal, rand
from client import Client


CLIENT_INCOME_MIN = 3000
CLIENT_INCOME_MAX = 50000


def generate_normal(lower: float, upper: float) -> float:
    mean = (upper + lower) / 2
    sigma = (upper - lower) / 6  # 3 sigma rule
    return max(lower, min(upper, normal(mean, sigma)))


def generate_uniform(lower: float, upper: float) -> float:
    return lower + rand() * (upper - lower)


class ServiceDurationGenerator:
    def __init__(self, distribution: str, min_minutes: int, max_minutes: int):
        if not (0 <= min_minutes <= max_minutes):
            raise ValueError('Incorrect interval!')
        if distribution not in {'normal', 'uniform'}:
            raise ValueError('Incorrect distribution!')
        self.__min_minutes = min_minutes
        self.__max_minutes = max_minutes
        self.__generator = generate_uniform if distribution == 'uniform' else generate_normal

    def get_duration(self) -> timedelta:
        return timedelta(minutes=self.__generator(self.__min_minutes, self.__max_minutes))


class ClientGenerator:
    def __init__(self, distribution: str, min_minutes: int, max_minutes: int, current_time: datetime):
        if not (0 <= min_minutes <= max_minutes):
            raise ValueError('Incorrect interval!')
        if distribution not in {'normal', 'uniform'}:
            raise ValueError('Incorrect distribution!')
        self.__min_minutes = min_minutes
        self.__max_minutes = max_minutes
        self.__generator = generate_uniform if distribution == 'uniform' else generate_normal
        self.start_new_day(current_time)

    def start_new_day(self, start_time: datetime) -> None:
        self.__client_no = 0
        self.__update_client_queue(start_time)

    def __update_client_queue(self, start_time: datetime) -> None:
        max_minutes = self.__max_minutes
        if start_time.weekday() >= 4 or start_time.hour > 16:  # higher frequency
            max_minutes -= (self.__max_minutes - self.__min_minutes) / 5
        self.__next_client_arrival = start_time + timedelta(minutes=self.__generator(self.__min_minutes, max_minutes))

    def check_for_client(self, current_time: datetime) -> Optional[Client]:
        if current_time < self.__next_client_arrival:
            return None
        self.__client_no += 1
        self.__update_client_queue(self.__next_client_arrival)
        client_income = self.__generator(CLIENT_INCOME_MIN, CLIENT_INCOME_MAX)
        return Client(self.__client_no, client_income)
