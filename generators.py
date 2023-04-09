from datetime import timedelta, datetime
from typing import Optional

from numpy.random import normal, rand

from client import Client
from config import CLIENT_INCOME_MIN, CLIENT_INCOME_MAX
from config import HIGHER_FREQUENCY_DAY, HIGHER_FREQUENCY_HOUR, HIGHER_FREQUENCY_DEMAND_INCREASE
from distribution import Distribution


def generate_normal(lower: float, upper: float) -> float:
    mean = (upper + lower) / 2
    sigma = (upper - lower) / 6  # 3 sigma rule
    return max(lower, min(upper, normal(mean, sigma)))


def generate_uniform(lower: float, upper: float) -> float:
    return lower + rand() * (upper - lower)


class ServiceDurationGenerator:
    def __init__(self, distribution: Distribution, min_minutes: int, max_minutes: int):
        if not (0 <= min_minutes <= max_minutes):
            raise ValueError('Incorrect interval!')
        self._min_minutes = min_minutes
        self._max_minutes = max_minutes
        self._generator = generate_uniform if distribution == Distribution.UNIFORM else generate_normal

    def get_duration(self) -> timedelta:
        return timedelta(minutes=self._generator(self._min_minutes, self._max_minutes))


class ClientGenerator:
    def __init__(self, distribution: Distribution, client_probability: float):
        self._client_probability = client_probability
        self._generator = generate_uniform if distribution == Distribution.UNIFORM else generate_normal
        self._client_no = 0

    def start_new_day(self) -> None:
        self._client_no = 0

    def check_for_client(self, current_time: datetime) -> Optional[Client]:
        client_probability = self._client_probability
        if current_time.weekday() >= HIGHER_FREQUENCY_DAY or current_time.hour > HIGHER_FREQUENCY_HOUR:
            client_probability *= HIGHER_FREQUENCY_DEMAND_INCREASE
        if rand() <= client_probability:
            self._client_no += 1
            client_income = self._generator(CLIENT_INCOME_MIN, CLIENT_INCOME_MAX)
            return Client(self._client_no, client_income)
