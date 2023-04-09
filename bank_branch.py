from collections import deque
from datetime import datetime

from clerk import Clerk
from client import Client
from config import CLERK_DAY_SALARY, TIMETABLE, LUNCH_START, LUNCH_END
from generators import ServiceDurationGenerator
from operation import Operation, QueueUpdate
from timetable import Timetable


class BankBranch:
    def __init__(self, clerk_count: int, queue_max_length: int,
                 service_generator: ServiceDurationGenerator, timetable: Timetable = None):
        if clerk_count <= 0 or queue_max_length <= 0:
            raise ValueError('Incorrect parameters!')
        self._clerk_count = clerk_count
        self._queue_max_length = queue_max_length
        self._service_generator = service_generator
        self._clerks = list()
        for clerk_no in range(self._clerk_count):
            self._clerks.append(Clerk(clerk_no))
        self._free_clerks = list(range(self._clerk_count))
        self._queue = deque()
        self._profit = -CLERK_DAY_SALARY * self._clerk_count
        self.timetable = timetable if timetable is not None else Timetable(TIMETABLE, LUNCH_START, LUNCH_END)

    def start_new_day(self) -> list[QueueUpdate]:
        updates = list()
        for clerk in self._clerks:
            if clerk.has_client is not None:
                updates.append((Operation.FINISH_SERVICE, clerk.id, clerk.has_client))
                clerk.has_client = None
        self._free_clerks = list(range(self._clerk_count))
        for client in self._queue:
            updates.append((Operation.LEAVE_QUEUE, client.id, -1))
        self._queue = deque()
        self._profit -= CLERK_DAY_SALARY * self._clerk_count
        return updates

    def add_client(self, client: Client) -> QueueUpdate:
        if len(self._queue) >= self._queue_max_length:
            return Operation.LEAVE_QUEUE, client.id, -1
        self._queue.append(client)
        return Operation.STAND_INTO_QUEUE, client.id, -1

    def update_situation(self, current_time: datetime) -> list[QueueUpdate]:
        updates = list()
        for clerk in self._clerks:
            if clerk.has_client is not None and clerk.service_ending < current_time:
                updates.append((Operation.FINISH_SERVICE, clerk.id, clerk.has_client))
                clerk.has_client = None
                self._free_clerks.append(clerk.id)
        while (not self.timetable.is_lunch(current_time)) and self._free_clerks and self._queue:
            first_client = self._queue.popleft()
            free_clerk = self._clerks[self._free_clerks.pop(0)]
            free_clerk.has_client = first_client.id
            free_clerk.service_ending = current_time + self._service_generator.get_duration()
            self._profit += first_client.income
            updates.append((Operation.START_SERVICE, free_clerk.id, first_client.id))
        return updates

    @property
    def profit(self) -> int:
        return self._profit
