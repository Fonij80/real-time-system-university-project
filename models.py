# Foroozan Iraji - 99105272
# Fatemeh Sadat Lajevardi - 400105217
from enum import Enum


class CriticalityLevel(Enum):
    S0 = 0
    S1 = 1
    S2 = 2
    S3 = 3

    def __init__(self, level):
        self.level = level

    def __lt__(self, other):
        return self.level < other.level

    def __eq__(self, other):
        return self.level == other.level

    def __hash__(self):
        return hash(self.level)

    def __repr__(self):
        return f"CriticalityLevel({self.level})"


class CriticalityStats:

    def __init__(self):
        self.task_count = 0
        self.total_response_time = 0
        self.missed_count = 0

    def count_number_of_task(self):
        self.task_count += 1

    def sum_response_time(self, response_time):
        self.total_response_time += response_time

    def count_missed_task(self):
        self.missed_count += 1

    def average_response_time(self):
        return self.total_response_time / self.task_count if self.task_count > 0 else 0


class Task:
    _counter = 0
    task_count_based_on_criticality = {CriticalityLevel.S0: CriticalityStats(),
                                       CriticalityLevel.S1: CriticalityStats(),
                                       CriticalityLevel.S2: CriticalityStats(),
                                       CriticalityLevel.S3: CriticalityStats()}

    def __init__(self, number_of_clocks: int, data_amount: int, deadline: int, criticality: CriticalityLevel,
                 arrival_time: int):
        self.id = Task._counter
        Task._counter += 1
        self.number_of_clocks = number_of_clocks  # ci
        self.data_amount = data_amount  # di
        self.deadline = deadline  # Ti
        self.criticality = criticality  # pi
        self.arrival_time = arrival_time  # equal to task's index in generated task list
        self.execution_time = 0
        self.productivity = 0
        self.response_time = 0  # finish time - arrival time
        self.is_missed = False
        self.server = None
        Task.task_count_based_on_criticality[criticality].count_number_of_task()

    def __str__(self):
        return (f"Task {self.id}, Productivity: {self.productivity}, Assigned Server: {self.server.id}, "
                f"Response time: {self.response_time}, Is missed: {self.is_missed}")

    @staticmethod
    def reset_static_fields():
        Task._counter = 0
        Task.task_count_based_on_criticality[CriticalityLevel.S0] = CriticalityStats()
        Task.task_count_based_on_criticality[CriticalityLevel.S1] = CriticalityStats()
        Task.task_count_based_on_criticality[CriticalityLevel.S2] = CriticalityStats()
        Task.task_count_based_on_criticality[CriticalityLevel.S3] = CriticalityStats()

    def get_execution_time(self, server):
        return int(self.number_of_clocks / server.processing_frequency)

    def get_sending_delay_to_server(self, server):
        return int(self.data_amount / server.data_transmission_rate)

    def get_productivity(self, server):
        return round(self.get_execution_time(server) / self.deadline, 2) * 10

    def update_after_assign(self, server):
        self.arrival_time += self.get_sending_delay_to_server(server)
        self.execution_time = self.number_of_clocks / server.processing_frequency
        self.server = server
        self.productivity = self.get_productivity(server)


class Server:
    _counter = 0

    def __init__(self, processing_frequency: int, data_transmission_rate: int, number_of_cores: int,
                 productivity: int = 0):
        self.id = Server._counter
        Server._counter += 1
        self.processing_frequency = processing_frequency  # fi
        self.data_transmission_rate = data_transmission_rate  # vi
        self.number_of_cores = number_of_cores  # zi
        self.productivity = productivity  # ui
        self.number_of_assigned_tasks = {CriticalityLevel.S0: 0, CriticalityLevel.S1: 0, CriticalityLevel.S2: 0,
                                         CriticalityLevel.S3: 0}
        self.assigned_tasks = []
        self.number_of_more_criticality_level = 0

    def __str__(self):
        return f"Server {self.id}, Productivity: {self.productivity}"

    def assign_task(self, task):
        self.assigned_tasks.append(task)  # task assigned successfully
        self.update_productivity()
        self.number_of_assigned_tasks[task.criticality] += 1
        # update task arrival_time based on transmission's delay between base station and server
        task.update_after_assign(self)

    def update_productivity(self):
        self.productivity = int(sum(t.get_productivity(self) for t in self.assigned_tasks))

    def execute_tasks(self, is_criticality_considered=False):
        # Sort assigned tasks based on arrival time
        sorted_tasks_based_on_arrival_time = sorted(self.assigned_tasks, key=lambda t: t.arrival_time)
        current_time = sorted_tasks_based_on_arrival_time[0].arrival_time
        arrived_tasks = []

        while sorted_tasks_based_on_arrival_time or arrived_tasks:
            # Check for new arrivals at the current time
            while sorted_tasks_based_on_arrival_time and sorted_tasks_based_on_arrival_time[
                0].arrival_time == current_time:
                arrived_tasks.append(sorted_tasks_based_on_arrival_time.pop(0))

            if not arrived_tasks:
                current_time = sorted_tasks_based_on_arrival_time[0].arrival_time
                continue  # Check for new arrivals at arrival time of first task in list

            # Process each arrived task in FIFO order
            for task in arrived_tasks:
                if not is_criticality_considered:
                    # Check if the deadline will be missed
                    if current_time + task.execution_time > task.deadline:
                        task.is_missed = True
                        Task.task_count_based_on_criticality[task.criticality].count_missed_task()
                        arrived_tasks.remove(task)  # Remove missed task from arrived tasks
                        continue
                    # Execute the task
                    current_time += task.execution_time  # Update current time after execution
                    task.response_time = current_time - task.arrival_time
                    Task.task_count_based_on_criticality[task.criticality].sum_response_time(task.response_time)
                    arrived_tasks.remove(task)  # Task executed successfully
                    self.update_productivity()  # Update server's productivity after executing the task
                    print(f'Task {task.id} arrived at {task.arrival_time}, finished at: {current_time}')

                else:  # Execute based on criticality level
                    sorted_arrived_tasks_based_on_criticality = sorted(arrived_tasks, key=lambda t: t.criticality.level)
                    # TODO
                    return


class BaseStation:
    def __init__(self):
        Server._counter = 0
        self.servers = []

    def add_server(self, server):
        self.servers.append(server)

    def create_schedule_table(self, tasks, isCriticalityLevelConsidered):
        for i in range(len(tasks)):
            # assign tasks based on server productivity
            sorted_servers_based_on_productivity = sorted(self.servers, key=lambda s: s.productivity)
            print(f"Task: {tasks[i].id}, clocks: {tasks[i].number_of_clocks}, arrival: {tasks[i].arrival_time}")
            for server in sorted_servers_based_on_productivity:
                print(f"Server: {server.id}, productivity: {server.productivity}")
                if server.productivity + tasks[i].get_productivity(server) <= server.number_of_cores:
                    server.assign_task(tasks[i])
                    print(
                        f"Task {tasks[i].id} assigned to Server {server.id}, task productivity: {tasks[i].get_productivity(server)}, cors: {server.number_of_cores} First if")
                    break  # go to next task
                elif not isCriticalityLevelConsidered:  # no server can meet the task's deadline
                    # assign task to server with the least productivity
                    print(f"Task {tasks[i].id} assigned to Server {server.id}, Second if")
                    sorted_servers_based_on_productivity[0].assign_task(tasks[i])
                    break  # go to next task
                else:  # schedule based on criticality level
                    server.number_of_more_criticality_level = 0
                    for criticality, number_of_tasks in server.number_of_assigned_tasks.items():
                        if criticality.value >= tasks[i].criticality.value:
                            server.number_of_more_criticality_level += number_of_tasks
                    # choose server with the least number of tasks with criticality more or equal to current task
                    sorted_servers = sorted(self.servers, key=lambda s: s.number_of_more_criticality_level)
                    sorted_servers[0].assign_task(tasks[i])
