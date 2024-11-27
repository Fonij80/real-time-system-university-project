from models import Task, Server, BaseStation, CriticalityLevel
import random
from matplotlib import pyplot as plt


def initialize_base_station(number_of_servers):
    station = BaseStation()
    # generate servers
    for _ in range(number_of_servers):
        frequency = random.uniform(1.0, 3.5)  # GHz
        transmission_rate = random.uniform(100.0, 1000.0)  # Mbps
        cores = random.randint(4, 16)
        station.add_server(Server(frequency, transmission_rate, cores))

    return station


def generate_tasks(number_of_tasks):
    tasks = []
    for _ in range(number_of_tasks):
        clocks = random.randint(1, 10) * 10
        data_amount = random.uniform(10.0, 500.0)  # MB
        deadline = random.randint(1, 100)
        criticality = random.choice(list(CriticalityLevel))
        tasks.append(Task(clocks, data_amount, deadline, criticality))

    return tasks


def simulate(number_of_servers, number_of_tasks):
    base_station = initialize_base_station(number_of_servers)
    tasks = generate_tasks(number_of_tasks)

    response_times = []

    for task in tasks:
        base_station.assign_task(task)
        response_times.append(
            task.number_of_clocks / sum(server.processing_frequency for server in base_station.servers))

    return response_times


def simulate_based_on_criticality():
    pass


if __name__ == "__main__":
    # response time
    num_tasks_list = [40, 80, 160, 320, 640]

    for num_tasks in num_tasks_list:
        response_times = simulate(4, num_tasks)
        print(response_times)

        plt.plot(response_times, label=f'Tasks: {num_tasks}')

    plt.title('Response Time ignoring criticality')
    plt.xlabel('Criticality')
    plt.ylabel('Response Time')
    plt.legend()
    plt.show()

    # response time by considering criticality

    # DMR

    # DMR by considering criticality

    # DMR by considering criticality and time
