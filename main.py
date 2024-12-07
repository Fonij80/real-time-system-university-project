from models import Task, Server, BaseStation, CriticalityLevel
import random
from matplotlib import pyplot as plt
import pandas as pd



arrival_time_counter = 0

def initialize_base_station(number_of_servers):
    station = BaseStation()
    # generate servers
    for _ in range(number_of_servers):
        frequency = random.uniform(1.0, 3.5)  # GHz
        transmission_rate = random.uniform(100.0, 1000.0)  # Mbps
        cores = random.randint(4, 16)
        station.add_server(Server(frequency, transmission_rate, cores))

    return station


def generate_tasks(number_of_tasks, criticality_level=None):
    tasks = []
    if criticality_level is None:  # if number of tasks is not based on their criticality
        Task.reset_static_fields()
    for i in range(number_of_tasks):
        clocks = random.randint(1, 10) * 10
        data_amount = random.uniform(10.0, 500.0)  # MB
        deadline = random.randint(i, 1000)
        criticality = criticality_level is not None if criticality_level else random.choice(list(CriticalityLevel))
        tasks.append(Task(clocks, data_amount, deadline, criticality, i))

    return tasks


def generate_tasks_based_on_criticality(number_of_tasks_based_on_criticality):
    tasks = []
    for criticality_level, number_of_tasks in number_of_tasks_based_on_criticality.items():
        tasks.append(generate_tasks(number_of_tasks, criticality_level))

    return tasks


def simulate(number_of_servers, tasks, isCriticalityLevelConsidered=False):
    base_station = initialize_base_station(number_of_servers)
    base_station.create_schedule_table(tasks, isCriticalityLevelConsidered)  # assign tasks based on specified criteria and create offline table

    for server in base_station.servers:  # run each task to get its response time and is_missed
        server.executeTasks()

    return tasks


if __name__ == "__main__":
    number_of_servers = 2

    # Phase 1 Outputs
    # 40, 80, 160, 320, 640 tasks
    for number in [40, 80, 160, 320, 640]:
        simulate(number_of_servers, generate_tasks(number))  # run simulation
        # Average Response Time By Criticality
        plt.figure(figsize=(10, 6))
        plt.bar([CriticalityLevel.S0.level, CriticalityLevel.S1.level,
                 CriticalityLevel.S2.level, CriticalityLevel.S3.level],
                [Task.task_count_based_on_criticality[CriticalityLevel.S0].total_response_time,
                 Task.task_count_based_on_criticality[CriticalityLevel.S1].total_response_time,
                 Task.task_count_based_on_criticality[CriticalityLevel.S2].total_response_time,
                 Task.task_count_based_on_criticality[CriticalityLevel.S3].total_response_time,],
                color=['red', 'orange', 'green'])
        plt.title('Average Response Time by Criticality Level')
        plt.xlabel('Criticality Level')
        plt.ylabel('Average Response Time (seconds)')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()

        # Deadline Miss Ratio By Criticality
        # missed_tasks = sum(task.is_missed for task in result_tasks)

    # 320 tasks: S0: 80, S1: 80, S2: 80, S3: 80
    number_of_tasks_based_on_criticality = {CriticalityLevel.S0: 80, CriticalityLevel.S1: 80, CriticalityLevel.S2: 80,
                                            CriticalityLevel.S3: 80}
    # simulate(number_of_servers, generate_tasks_based_on_criticality(number_of_tasks_based_on_criticality))
    # Average Response Time By Criticality
    # Deadline Miss Ratio By Criticality
    # Deadline Miss Ratio By Criticality with Ltotal / 40
    # Deadline Miss Ratio By Criticality with Ltotal / 20
    # Deadline Miss Ratio By Criticality with Ltotal / 5

    # 320 tasks: S0: 100, S1: 80, S2: 80, S3: 60
    number_of_tasks_based_on_criticality = {CriticalityLevel.S0: 100, CriticalityLevel.S1: 80, CriticalityLevel.S2: 80,
                                            CriticalityLevel.S3: 60}
    # simulate(number_of_servers, generate_tasks_based_on_criticality(number_of_tasks_based_on_criticality))
    # Average Response Time By Criticality
    # Deadline Miss Ratio By Criticality

    # 320 tasks: S0: 150, S1: 80, S2: 80, S3: 10
    number_of_tasks_based_on_criticality = {CriticalityLevel.S0: 150, CriticalityLevel.S1: 80, CriticalityLevel.S2: 80,
                                            CriticalityLevel.S3: 10}
    # simulate(number_of_servers, generate_tasks_based_on_criticality(number_of_tasks_based_on_criticality))
    # Average Response Time By Criticality
    # Deadline Miss Ratio By Criticality

    # TODO plot below outputs
    # Phase 2 Outputs
    # Average Response Time By Criticality with 40, 80, 160, 320, 640 tasks

    # Deadline Miss Ratio By Criticality with 40, 80, 160, 320, 640 tasks
