from enum import Enum


class BagStatus(Enum):
    OK = 1,
    LOOKAHEAD_EXCEEDED = 2,
    NO_MORE_FRUITS = 3
