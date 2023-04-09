from dataclasses import dataclass

from operation import Operation, QueueUpdate


@dataclass
class Stats:
    iteration: int = 0
    minutes_passed: int = 0
    queue_length: int = 0
    clerks_occupied: int = 0
    clients_served: int = 0
    clients_lost: int = 0
    avg_queue_length: float = 0.
    max_queue_length: int = 0
    _total_wait_time_minutes: int = 0
    avg_waiting_time_minutes: float = 0.
    _total_clerk_occupied_minutes: int = 0
    avg_clerk_utilization: float = 0.

    def __init__(self, step_size_minutes: int, clerk_count: int):
        self._step_size_minutes = step_size_minutes
        self._clerk_count = clerk_count

    def start_new_day(self) -> None:
        self.queue_length = 0
        self.clerks_occupied = 0

    def update(self, updates: list[QueueUpdate]) -> None:
        self.iteration += 1
        self.minutes_passed += self._step_size_minutes
        for update in updates:
            if update[0] == Operation.STAND_INTO_QUEUE:
                self.queue_length += 1
                self.max_queue_length = max(self.max_queue_length, self.queue_length)
            if update[0] == Operation.START_SERVICE:
                self.queue_length -= 1
                self.clerks_occupied += 1
            if update[0] == Operation.FINISH_SERVICE:
                self.clients_served += 1
                self.clerks_occupied -= 1
            if update[0] == Operation.LEAVE_QUEUE:
                self.clients_lost += 1
        self._total_wait_time_minutes += self.queue_length * self._step_size_minutes
        if self.clerks_occupied + self.clients_served + self.queue_length != 0:
            self.avg_waiting_time_minutes = self._total_wait_time_minutes / \
                (self.clerks_occupied + self.clients_served + self.queue_length)
        self._total_clerk_occupied_minutes += self.clerks_occupied * self._step_size_minutes
        self.avg_clerk_utilization = self._total_clerk_occupied_minutes / (self.minutes_passed * self._clerk_count)
        self.avg_queue_length = (self.avg_queue_length * (self.iteration - 1) + self.queue_length) / self.iteration
