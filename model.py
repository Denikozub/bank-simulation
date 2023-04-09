from datetime import timedelta, datetime, date

from bank_branch import BankBranch
from generators import ClientGenerator, ServiceDurationGenerator, Distribution
from operation import QueueUpdate
from stats import Stats


class Model:
    def __init__(self, clerk_count: int, distribution: Distribution, client_probability: float,
                 service_min_minutes: int, service_max_minutes: int, queue_max_length: int,
                 step_size_minutes: int, simulation_end: date):
        if step_size_minutes <= 0:
            raise ValueError('Incorrect step size!')
        service_generator = ServiceDurationGenerator(distribution, service_min_minutes, service_max_minutes)
        self._bank = BankBranch(clerk_count, queue_max_length, service_generator)
        self._client_generator = ClientGenerator(distribution, client_probability)
        self._stats = Stats(step_size_minutes, clerk_count)
        self._step_size = timedelta(minutes=step_size_minutes)
        self._simulation_end = simulation_end
        self._current_time = datetime.now() + timedelta(hours=3)

    def step(self) -> list[QueueUpdate]:
        self._current_time += self._step_size
        if not self._bank.timetable.is_working(self._current_time):  # skip to new day
            self._current_time = self._bank.timetable.get_next_day_start(self._current_time)
            self._client_generator.start_new_day()
            updates = self._bank.start_new_day()
            self._stats.update(updates)
            self._stats.start_new_day()
            return updates

        updates = list()
        client = self._client_generator.check_for_client(self._current_time)
        if client is not None:
            updates.append(self._bank.add_client(client))
        updates.extend(self._bank.update_situation(self._current_time))
        self._stats.update(updates)
        return updates

    def simulate(self) -> list[list[QueueUpdate]]:
        updates = list()
        while self._current_time.date() != self._simulation_end:
            updates.append(self.step())
        return updates

    @property
    def stats(self) -> Stats:
        return self._stats

    @property
    def current_profit(self) -> int:
        return self._bank.profit

    @property
    def current_time(self) -> datetime:
        return self._current_time
