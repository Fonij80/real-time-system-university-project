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
    task_count_based_on_criticality = {CriticalityLevel.S0: CriticalityStats(),
                                       CriticalityLevel.S1: CriticalityStats(),
                                       CriticalityLevel.S2: CriticalityStats(),
                                       CriticalityLevel.S3: CriticalityStats()}

    def __init__(self, number_of_clocks: int, data_amount: float, deadline: int, criticality: CriticalityLevel,
                 arrival_time: int):
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

    @staticmethod
    def reset_static_fields():
        Task.task_count_based_on_criticality = {
            CriticalityLevel.S0: CriticalityStats(),
            CriticalityLevel.S1: CriticalityStats(),
            CriticalityLevel.S2: CriticalityStats(),
            CriticalityLevel.S3: CriticalityStats()
        }

    def execute(self, current_time):
        finish_time = current_time + self.execution_time
        self.response_time = finish_time - self.arrival_time
        Task.task_count_based_on_criticality[self.criticality].sum_response_time(self.response_time)
        return finish_time

    def get_execution_time(self, server):
        """محاسبه زمان اجرا بر اساس فرکانس سرور"""
        return self.number_of_clocks / server.processing_frequency

    def get_sending_delay_to_server(self, server):
        """محاسبه تأخیر ارسال داده‌ها به سرور"""
        return self.data_amount / server.data_transmission_rate

    def get_productivity(self, server):
        """محاسبه بهره‌وری وظیفه بر روی یک سرور"""
        return self.get_execution_time(server) / self.deadline


class Server:
    _counter = 0

    def __init__(self, processing_frequency: float, data_transmission_rate: float, number_of_cores: int,
                 productivity: float = 0):
        self.id = Server._counter
        Server._counter += 1
        self.processing_frequency = processing_frequency  # fi
        self.data_transmission_rate = data_transmission_rate  # vi
        self.number_of_cores = number_of_cores  # zi
        self.productivity = productivity  # ui
        self.number_of_assigned_tasks = {CriticalityLevel.S0: 0, CriticalityLevel.S1: 0, CriticalityLevel.S2: 0,
                                         CriticalityLevel.S3: 0}
        self.assigned_tasks = []

    def assign_task(self, task):
        self.assigned_tasks.append(task)  # task assigned successfully
        self.update_productivity()
        self.number_of_assigned_tasks[task.criticality] += 1
        task.execution_time = task.number_of_clocks / self.processing_frequency

    def update_productivity(self):
        self.productivity = sum(t.productivity for t in self.assigned_tasks)

    def executeTasks(self, isCriticalityConsidered=False):
        sorted_tasks_based_on_arrival_time = sorted(self.assigned_tasks, key=lambda t: t.arrival_time)
        current_time = 0
        while sorted_tasks_based_on_arrival_time:
            if isCriticalityConsidered:
                # Sort based on criticality level first
                sorted_tasks_based_on_arrival_time = sorted(sorted_tasks_based_on_arrival_time,
                                                            key=lambda t: t.criticality.level)
            task = sorted_tasks_based_on_arrival_time.pop(0)
            if current_time + task.execution_time > task.deadline:
                task.is_missed = True
                Task.task_count_based_on_criticality[task.criticality].count_missed_task()
                continue
            current_time = task.execute(current_time)
            self.update_productivity()


class BaseStation:
    def __init__(self):
        self.servers = []

    def add_server(self, server):
        self.servers.append(server)

    def create_schedule_table(self, tasks, isCriticalityLevelConsidered):
        # assign tasks based on server productivity
        sorted_servers_based_on_productivity = sorted(self.servers, key=lambda s: s.productivity)

        for task in tasks:
            for server in sorted_servers_based_on_productivity:
                if server.productivity + task.get_productivity(server) <= server.number_of_cores:
                    server.assign_task(task)
                    break
