from enum import Enum
from datetime import datetime, time
from timetable import Timetable
from generators import ServiceDurationGenerator
from clerk import Clerk
from client import Client


class Operation(Enum):
    LEAVE_QUEUE = 1
    STAND_INTO_QUEUE = 2
    START_SERVICE = 3
    FINISH_SERVICE = 4


CLERK_DAY_SALARY = 2000
TIMETABLE = [
    (time(hour=10), time(hour=19)),
    (time(hour=10), time(hour=19)),
    (time(hour=10), time(hour=19)),
    (time(hour=10), time(hour=19)),
    (time(hour=10), time(hour=19)),
    (time(hour=11), time(hour=18)),
    (None, None),
]
LUNCH_START = time(hour=13)
LUNCH_END = time(hour=14)


class BankBranch:
    timetable = Timetable(TIMETABLE, LUNCH_START, LUNCH_END)

    def __init__(self, clerk_count: int, queue_max_length: int, service_generator: ServiceDurationGenerator):
        if clerk_count <= 0 or queue_max_length <= 0:
            raise ValueError('Incorrect parameters!')
        self.__clerk_count = clerk_count
        self.__queue_max_length = queue_max_length
        self.__service_generator = service_generator
        self.__clerks = list()
        for clerk_no in range(self.__clerk_count):
            self.__clerks.append(Clerk(clerk_no))
        self.__free_clerks = list(range(self.__clerk_count))
        self.__queue = list()
        self.__profit = -CLERK_DAY_SALARY * self.__clerk_count

    def start_new_day(self) -> list[tuple[Operation, int, int]]:
        updates = list()
        for clerk in self.__clerks:
            if clerk.has_client is not None:
                updates.append((Operation.FINISH_SERVICE, clerk.id, clerk.has_client))
                clerk.has_client = None
        self.__free_clerks = list(range(self.__clerk_count))
        for client in self.__queue:
            updates.append((Operation.LEAVE_QUEUE, client.id, -1))
        self.__queue = list()
        self.__profit -= CLERK_DAY_SALARY * self.__clerk_count
        return updates

    def add_client(self, client: Client) -> tuple[Operation, int, int]:
        if len(self.__queue) >= self.__queue_max_length:
            return Operation.LEAVE_QUEUE, client.id, -1
        self.__queue.append(client)
        return Operation.STAND_INTO_QUEUE, client.id, -1

    def update_situation(self, current_time: datetime) -> list[tuple[Operation, int, int]]:
        updates = list()
        for clerk in self.__clerks:
            if clerk.has_client is not None and clerk.service_ending < current_time:
                updates.append((Operation.FINISH_SERVICE, clerk.id, clerk.has_client))
                clerk.has_client = None
                self.__free_clerks.append(clerk.id)
        while self.__free_clerks and self.__queue:
            first_client = self.__queue.pop(0)
            free_clerk = self.__clerks[self.__free_clerks.pop(0)]
            free_clerk.has_client = first_client.id
            free_clerk.service_ending = current_time + self.__service_generator.get_duration()
            self.__profit += first_client.income
            updates.append((Operation.START_SERVICE, free_clerk.id, first_client.id))
        return updates

    def get_current_profit(self) -> int:
        return self.__profit
