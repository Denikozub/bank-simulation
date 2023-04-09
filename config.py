from datetime import time

CLIENT_INCOME_MIN = 50
CLIENT_INCOME_MAX = 3000
CLERK_DAY_SALARY = 2000

HIGHER_FREQUENCY_DAY = 4
HIGHER_FREQUENCY_HOUR = 16
HIGHER_FREQUENCY_DEMAND_INCREASE = 1.2

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

CLERK_COUNT_START_VALUE = 3
CLERK_COUNT_RANGE = [2, 7]
DISTRIBUTIONS = ['uniform', 'normal']
SERVICE_MIN_MIN = 0
SERVICE_MIN_START = 10
SERVICE_MIN_STEP = 1
SERVICE_MAX_START = 30
SERVICE_MAX_STEP = 1
QUEUE_LENGTH_RANGE = [5, 20]
QUEUE_LENGTH_START = 10
STEP_SIZE_RANGE = [1, 20]
STEP_SIZE_DEFAULT = 2
PROBABILITY_START_VALUE = 0.2
SIM_DEFAULT_DURATION_DAYS = 30
