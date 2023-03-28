from datetime import timedelta, datetime
from bank_branch import BankBranch, Operation
from generators import ClientGenerator, ServiceDurationGenerator
from stats import Stats


class Model:
    def __init__(self, clerk_count: int, distribution: str, client_min_minutes: int,
                 client_max_minutes: int, service_min_minutes: int, service_max_minutes: int,
                 queue_max_length: int, step_size_minutes: int, step_count: int):
        if step_size_minutes <= 0:
            raise ValueError('Incorrect step size!')
        service_generator = ServiceDurationGenerator(distribution, service_min_minutes, service_max_minutes)
        self.__bank = BankBranch(clerk_count, queue_max_length, service_generator)
        self.__client_generator = ClientGenerator(distribution, client_min_minutes, client_max_minutes, datetime.now())
        self.__stats = Stats(step_size_minutes, clerk_count)
        self.__step_size = timedelta(minutes=step_size_minutes)
        self.__step_count_left = step_count
        self.__current_time = datetime.now()

    def step(self) -> list[tuple[Operation, int, int]]:
        self.__step_count_left -= 1
        self.__current_time += self.__step_size
        if not self.__bank.timetable.is_working(self.__current_time):  # skip to new day
            self.__current_time = self.__bank.timetable.get_next_day_start(self.__current_time)
            self.__client_generator.start_new_day(self.__current_time)
            updates = self.__bank.start_new_day()
            self.__stats.update(updates)
            self.__stats.start_new_day()
            return updates

        updates = list()
        client = self.__client_generator.check_for_client(self.__current_time)
        if client is not None:
            updates.append(self.__bank.add_client(client))
        updates.extend(self.__bank.update_situation(self.__current_time))
        self.__stats.update(updates)
        return updates

    def simulate(self) -> list[list[tuple[Operation, int, int]]]:
        return [self.step() for _ in range(self.__step_count_left)]

    def get_stats(self) -> Stats:
        return self.__stats

    def get_current_profit(self) -> int:
        return self.__bank.get_current_profit()

    def get_current_time(self) -> datetime:
        return self.__current_time
