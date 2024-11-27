from enum import Enum


class CriticalityLevel(Enum):
    S0 = 0
    S1 = 1
    S2 = 2
    S3 = 3


class Task:
    def __init__(self, number_of_clocks: int, data_amount: float, deadline: int, criticality: CriticalityLevel):
        self.number_of_clocks = number_of_clocks  # ci
        self.data_amount = data_amount  # di
        self.deadline = deadline  # Ti
        self.criticality = criticality  # pi


class Server:
    def __init__(self, processing_frequency: float, data_transmission_rate: float, number_of_cores: int,
                 productivity: float = 0):
        self.processing_frequency = processing_frequency  # fi
        self.data_transmission_rate = data_transmission_rate  # vi
        self.number_of_cores = number_of_cores  # zi
        self.productivity = productivity  # ui
        self.number_of_assigned_tasks = {CriticalityLevel.S0: 0, CriticalityLevel.S1: 0, CriticalityLevel.S2: 0,
                                         CriticalityLevel.S3: 0}


class BaseStation:
    def __init__(self):
        self.servers = []

    def add_server(self, server):
        self.servers.append(server)

    def assign_task(self, task):
        # assign tasks based on server productivity
        sorted_servers = sorted(self.servers, key=lambda s: s.productivity)

        for server in sorted_servers:
            if server.productivity + task.number_of_clocks <= server.number_of_cores:
                server.productivity += task.number_of_clocks  # task assigned successfully
                server.number_of_assigned_tasks[task.criticality] += 1
                return 0
            server.number_of_more_criticality_level = 0
            for criticality, number_of_tasks in server.number_of_assigned_tasks.items():
                if criticality.value >= task.criticality.value:
                    server.number_of_more_criticality_level += number_of_tasks

        # no server can meet the task's deadline
        sorted_servers = sorted(self.servers, key=lambda s: s.number_of_more_criticality_level)
        sorted_servers[0].productivity += task.number_of_clocks  # task assigned successfully
        sorted_servers[0].number_of_assigned_tasks[task.criticality] += 1
        return 1

    def assign_task_based_on_criticality(self, task):
        pass
