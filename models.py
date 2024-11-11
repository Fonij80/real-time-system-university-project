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


class Server:
    def __init__(self, processing_frequency: float, data_transmission_rate: float, number_of_cores: int,
                 productivity: float):
        self.processing_frequency = processing_frequency
        self.data_transmission_rate = data_transmission_rate
        self.number_of_cores = number_of_cores
        self.productivity = productivity


class BaseStation:
    def __init__(self):
        self.servers = []

    def add_server(self, server):
        self.servers.append(server)

    def allocate_task(self, task):
        # Sort servers by productivity (least productive first)
        sorted_servers = sorted(self.servers, key=lambda s: s.productivity)

        for server in sorted_servers:
            if server.productivity + task.clocks <= server.cores:
                server.productivity += task.clocks
                return True  # Task allocated successfully

        return False  # No suitable server found
