from enum import Enum


class CriticalityLevel(Enum):
    S0 = "S0"
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"


class Task:
    def __init__(self, number_of_clocks: int, data_amount: float, deadline: str, criticality: CriticalityLevel):
        self.number_of_clocks = number_of_clocks
        self.data_amount = data_amount
        self.deadline = deadline
        self.criticality = criticality
