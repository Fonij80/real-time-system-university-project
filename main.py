# Foroozan Iraji - 99105272
# Fatemeh Sadat Lajevardi - 400105217
from models import Task, Server, BaseStation, CriticalityLevel
import random
from matplotlib import pyplot as plt

arrival_time_counter = 0


def generate_tasks(number_of_tasks, criticality_level=None):
    tasks = []
    if criticality_level is None:  # if number of tasks is not based on their criticality
        Task.reset_static_fields()

    for i in range(number_of_tasks):
        number_of_clocks = random.randint(1, 10) * 10
        data_amount = int(random.uniform(500.0, 1000.0))  # bit
        deadline = random.randint(i, 1000)
        criticality = criticality_level if criticality_level is not None else random.choice(list(CriticalityLevel))
        tasks.append(Task(number_of_clocks, data_amount, deadline, criticality, i))

    return tasks


def generate_tasks_based_on_criticality(number_of_tasks_based_on_criticality):
    tasks = []
    for criticality_level, number_of_tasks in number_of_tasks_based_on_criticality.items():
        tasks.append(generate_tasks(number_of_tasks, criticality_level))

    return tasks


def initialize_base_station(number_of_servers):
    station = BaseStation()

    # generate servers
    for i in range(number_of_servers):
        # how many cycles per second server can process
        processing_frequency = random.randint(1, 10)  # Hz
        data_transmission_rate = int(random.uniform(10.0, 100.0))  # bps
        number_of_cores = random.randint(1, 5)
        s = Server(processing_frequency, data_transmission_rate, number_of_cores)
        station.add_server(s)
        print(f"server: {s.id}, freq: {s.processing_frequency}, trans rate: {s.data_transmission_rate}, "
              f"cors: {s.number_of_cores}")

    return station


def simulate(number_of_servers, tasks, isCriticalityLevelConsidered=False):
    base_station = initialize_base_station(number_of_servers)
    # assign tasks based on specified criteria and create offline table
    base_station.create_schedule_table(tasks, isCriticalityLevelConsidered)

    for server in base_station.servers:  # run each task to get its response time and is_missed
        server.execute_tasks(isCriticalityLevelConsidered)


def plot_response_time_by_criticality_level(label):
    avg_response_times = [
        Task.task_count_based_on_criticality[level].total_response_time /
        Task.task_count_based_on_criticality[level].task_count
        for level in CriticalityLevel
    ]

    plt.figure(figsize=(10, 6))
    plt.bar([level.name for level in CriticalityLevel], avg_response_times,
            color=['red', 'orange', 'green', 'blue'])
    plt.title(f'Average Response Time by Criticality Level, {label}')
    plt.xlabel('Criticality Level')
    plt.ylabel('Average Response Time')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()


def plot_deadline_miss_ratio_by_criticality_level(label):
    miss_ratio = [
        Task.task_count_based_on_criticality[level].missed_count /
        Task.task_count_based_on_criticality[level].task_count
        for level in CriticalityLevel
    ]

    plt.figure(figsize=(10, 6))
    plt.bar([level.name for level in CriticalityLevel], miss_ratio,
            color=['red', 'orange', 'green', 'blue'])
    plt.title(f'Deadline Miss Ratio by Criticality Level, {label}')
    plt.xlabel('Criticality Level')
    plt.ylabel('Number of missed tasks / Number of whole tasks')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()


if __name__ == "__main__":
    number_of_servers = 4

    # Phase 1 Outputs: Ignoring Criticality Level
    for number in [40, 80, 160, 320, 640]:
        tasks = generate_tasks(number)
        simulate(number_of_servers, tasks)
        plot_response_time_by_criticality_level(label=f"for {number} tasks, Ignored Criticality")
        plot_deadline_miss_ratio_by_criticality_level(label=f"for {number} tasks, Ignored Criticality")

    # 320 tasks: S0: 80, S1: 80, S2: 80, S3: 80
    number_of_tasks_based_on_criticality = {CriticalityLevel.S0: 80, CriticalityLevel.S1: 80,
                                            CriticalityLevel.S2: 80,
                                            CriticalityLevel.S3: 80}
    generate_tasks_based_on_criticality(number_of_tasks_based_on_criticality)
    simulate(number_of_servers, tasks, isCriticalityLevelConsidered=True)
    plot_response_time_by_criticality_level(
        label="for 320 tasks: S0: 80, S1: 80, S2: 80, S3: 80 tasks, Considered Criticality")
    plot_deadline_miss_ratio_by_criticality_level(
        label="for 320 tasks: S0: 80, S1: 80, S2: 80, S3: 80 tasks, Considered Criticality")

    # TODO
    # Deadline Miss Ratio By Criticality with Ltotal / 40
    # Deadline Miss Ratio By Criticality with Ltotal / 20
    # Deadline Miss Ratio By Criticality with Ltotal / 5

    # 320 tasks: S0: 100, S1: 80, S2: 80, S3: 60
    number_of_tasks_based_on_criticality = {CriticalityLevel.S0: 100, CriticalityLevel.S1: 80,
                                            CriticalityLevel.S2: 80,
                                            CriticalityLevel.S3: 60}
    generate_tasks_based_on_criticality(number_of_tasks_based_on_criticality)
    simulate(number_of_servers, tasks, isCriticalityLevelConsidered=True)
    plot_response_time_by_criticality_level(
        label="for 320 tasks: S0: 100, S1: 80, S2: 80, S3: 60 tasks, Considered Criticality")
    plot_deadline_miss_ratio_by_criticality_level(
        label="for 320 tasks: S0: 100, S1: 80, S2: 80, S3: 60 tasks, Considered Criticality")

    # 320 tasks: S0: 150, S1: 80, S2: 80, S3: 10
    number_of_tasks_based_on_criticality = {CriticalityLevel.S0: 150, CriticalityLevel.S1: 80,
                                            CriticalityLevel.S2: 80,
                                            CriticalityLevel.S3: 10}
    generate_tasks_based_on_criticality(number_of_tasks_based_on_criticality)
    simulate(number_of_servers, tasks, isCriticalityLevelConsidered=True)
    plot_response_time_by_criticality_level(
        label="for 320 tasks: S0: 150, S1: 80, S2: 80, S3: 10 tasks, Considered Criticality")
    plot_deadline_miss_ratio_by_criticality_level(
        label="for 320 tasks: S0: 150, S1: 80, S2: 80, S3: 10 tasks, Considered Criticality")

    # Phase 2 Outputs: Considering Criticality Level
    for number in [40, 80, 160, 320, 640]:
        tasks = generate_tasks(number)
        simulate(number_of_servers, tasks, isCriticalityLevelConsidered=True)
        plot_response_time_by_criticality_level(label=f"for {number} tasks, Considered Criticality")
        plot_deadline_miss_ratio_by_criticality_level(label=f"for {number} tasks, Considered Criticality")
