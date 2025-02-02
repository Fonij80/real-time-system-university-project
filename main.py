# Foroozan Iraji - 99105272
# Fatemeh Sadat Lajevardi - 400105217
from models import Task, Server, BaseStation, CriticalityLevel
import random
import matplotlib
import copy
matplotlib.use('TkAgg')

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

def calculate_Ltotal():
    return sum(task.calculate_laxity() for level in CriticalityLevel for task in tasks if task.criticality == level)

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


def plot_laxity_by_criticality_level(label, tasks):
    avg_laxities = []
    for level in CriticalityLevel:
        total_laxity = 0
        task_count = Task.task_count_based_on_criticality[level].task_count
        if task_count > 0:
            for task in tasks:
                if task.criticality == level:
                    total_laxity += task.calculate_laxity()
            avg_laxities.append(total_laxity / task_count)
        else:
            avg_laxities.append(0)

    plt.figure(figsize=(10, 6))
    plt.bar([level.name for level in CriticalityLevel], avg_laxities,
            color=['red', 'orange', 'green', 'blue'])
    plt.title(f'Average Laxity by Criticality Level, {label}')
    plt.xlabel('Criticality Level')
    plt.ylabel('Average Laxity')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()


def plot_laxity_by_criticality_level(label, tasks):
    avg_laxities = []
    for level in CriticalityLevel:
        total_laxity = 0
        task_count = sum(1 for task in tasks if task.criticality == level)  # شمارش تعداد وظایف مربوط به هر سطح بحرانیت
        if task_count > 0:
            for task in tasks:
                if task.criticality == level:
                    total_laxity += task.calculate_laxity()
            avg_laxities.append(total_laxity / task_count)
        else:
            avg_laxities.append(0)

    plt.figure(figsize=(10, 6))
    plt.bar([level.name for level in CriticalityLevel], avg_laxities,
            color=['red', 'orange', 'green', 'blue'])
    plt.title(f'Average Laxity by Criticality Level, {label}')
    plt.xlabel('Criticality Level')
    plt.ylabel('Average Laxity')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()


if __name__ == "__main__":
    number_of_servers = 4

    for number in [40, 80, 160, 320, 640]:
        original_tasks = generate_tasks(number)

        tasks_without_criticality = copy.deepcopy(original_tasks)
        tasks_with_criticality = copy.deepcopy(original_tasks)

        print(f"Simulating for {number} tasks without considering criticality...")
        simulate(number_of_servers, tasks_without_criticality, isCriticalityLevelConsidered=False)
        plot_response_time_by_criticality_level(f"for {number} tasks, Ignored Criticality")
        plot_deadline_miss_ratio_by_criticality_level(f"for {number} tasks, Ignored Criticality")

        print(f"Simulating for {number} tasks considering criticality...")
        simulate(number_of_servers, tasks_with_criticality, isCriticalityLevelConsidered=True)
        plot_response_time_by_criticality_level(f"for {number} tasks, Considered Criticality")
        plot_deadline_miss_ratio_by_criticality_level(f"for {number} tasks, Considered Criticality")

        # اصلاح فراخوانی تابع بدون ارسال نام آرگومان (ارسال به‌صورت positional argument)
        plot_laxity_by_criticality_level(f"for {number} tasks, Considered Criticality", tasks_with_criticality)
