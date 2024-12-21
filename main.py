import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Task, Server, BaseStation, CriticalityLevel
import random
from matplotlib import pyplot as plt

random.seed(42)


def initialize_base_station(number_of_servers):
    station = BaseStation()
    for _ in range(number_of_servers):
        frequency = random.uniform(1.0, 3.5)  # GHz
        transmission_rate = random.uniform(100.0, 1000.0)  # Mbps
        cores = random.randint(4, 16)
        station.add_server(Server(frequency, transmission_rate, cores))
    return station


def generate_tasks(number_of_tasks, criticality_level=None):
    tasks = []
    Task.reset_static_fields()
    for i in range(number_of_tasks):
        clocks = random.randint(1, 10) * 10
        data_amount = random.uniform(10.0, 500.0)  # MB
        deadline = random.randint(100, 1000)
        criticality = criticality_level if criticality_level else random.choice(list(CriticalityLevel))
        tasks.append(Task(clocks, data_amount, deadline, criticality, i))
    return tasks


def simulate(number_of_servers, tasks, isCriticalityLevelConsidered=False):
    base_station = initialize_base_station(number_of_servers)
    base_station.create_schedule_table(tasks, isCriticalityLevelConsidered)

    for server in base_station.servers:
        server.executeTasks(isCriticalityLevelConsidered)

    return tasks


if __name__ == "__main__":
    number_of_servers = 2
    for number in [40, 80, 160, 320, 640]:
        tasks = generate_tasks(number)
        simulate(number_of_servers, tasks)

        plt.figure(figsize=(10, 6))
        plt.bar(
            [CriticalityLevel.S0.level, CriticalityLevel.S1.level,
             CriticalityLevel.S2.level, CriticalityLevel.S3.level],
            [Task.task_count_based_on_criticality[CriticalityLevel.S0].average_response_time(),
             Task.task_count_based_on_criticality[CriticalityLevel.S1].average_response_time(),
             Task.task_count_based_on_criticality[CriticalityLevel.S2].average_response_time(),
             Task.task_count_based_on_criticality[CriticalityLevel.S3].average_response_time()],
            color=['red', 'orange', 'green', 'blue']
        )
        plt.title(f'Average Response Time by Criticality Level for {number} Tasks')
        plt.xlabel('Criticality Level')
        plt.ylabel('Average Response Time (seconds)')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()
