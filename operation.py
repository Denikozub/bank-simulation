from enum import Enum


class Operation(Enum):
    LEAVE_QUEUE = 1
    STAND_INTO_QUEUE = 2
    START_SERVICE = 3
    FINISH_SERVICE = 4


QueueUpdate = tuple[Operation, int, int]
"""
Queue update info about each operation:
1) Operation = LEAVE_QUEUE:
    QueueUpdate[1]: client_no (int)
    QueueUpdate[2]: not used (-1)
2) Operation = STAND_INTO_QUEUE:
    QueueUpdate[1]: client_no (int)
    QueueUpdate[2]: not used (-1)
3) Operation = START_SERVICE:
    QueueUpdate[1]: clerk_no (int)
    QueueUpdate[2]: client_no (int)
4) Operation = FINISH_SERVICE:
    QueueUpdate[1]: clerk_no (int)
    QueueUpdate[2]: client_no (int)
"""
