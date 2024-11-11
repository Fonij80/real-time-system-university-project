from models import Task, Server, BaseStation, CriticalityLevel
import random
from matplotlib import pyplot as plt


def simulate(num_tasks):
    base_station = BaseStation()

    # Create some servers with random attributes
    for _ in range(5):
        frequency = random.uniform(1.0, 3.5)  # GHz
        transmission_rate = random.uniform(100.0, 1000.0)  # Mbps
        cores = random.randint(4, 16)
        base_station.add_server(Server(frequency, transmission_rate, cores))

    tasks = []

    # Generate tasks with random attributes
    for _ in range(num_tasks):
        clocks = random.randint(1, 10) * 10  # Random number of clocks (10-100)
        data_amount = random.uniform(10.0, 500.0)  # Random data amount (MB)
        deadline = random.randint(1, 100)  # Random deadline (time units)
        criticality = random.choice(list(CriticalityLevel))  # Random criticality level
        tasks.append(Task(clocks, data_amount, deadline, criticality))

    response_times = []

    for task in tasks:
        success = base_station.allocate_task(task)

        if success:
            response_times.append(task.clocks / sum(
                server.frequency for server in base_station.servers))  # Simplified response time calculation

    return response_times


if __name__ == "__main__":
    # response time
    num_tasks_list = [40, 80, 160, 320, 640]

    for num_tasks in num_tasks_list:
        response_times = simulate(num_tasks)

        plt.plot(response_times, label=f'Tasks: {num_tasks}')

    plt.title('Response Time vs Number of Tasks')
    plt.xlabel('Task Index')
    plt.ylabel('Response Time (arbitrary units)')
    plt.legend()
    plt.show()

    # response time with specific criticality

    # DMR

    # DMR with specific criticality

    # DMR with specific criticality and time
