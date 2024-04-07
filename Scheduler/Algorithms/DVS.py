from classes import Task, BaseAlgo, CPU
from math import gcd
import copy

class DVS(BaseAlgo):
    def Run(self, cpu: CPU, tasks: list[Task]):
        # create scm wcet schedule
        lcm = tasks[0].period
        for task in tasks:
            lcm = lcm * task.period // gcd(lcm, task.period)
        
        # sum_of_exec = 0
        # for task in tasks:
        #     for i in range(0, lcm, task.period):
        #         cpu.sort_push_back(Task(i, task.period, task.WCET, task.AET), key=lambda x: (x.arrival_time, x.arrival_time + x.period))
        #         sum_of_exec += task.WCET

        # print(cpu.QueueStr())
        # print(sum_of_exec)
        
        tasks = sorted(tasks, key=lambda x: (x.arrival_time, x.arrival_time + x.period))

        cpu.LOG("Start work")

        end_searching_time = 0
        searching_deadline = None
        unprocessed_tasks = copy.deepcopy(tasks)
        tasks_in_progress = []
        
        while len(unprocessed_tasks):
            for task in unprocessed_tasks:
                if self.time <= task.arrival_time <= end_searching_time:
                    tasks_in_progress.append(task)
                    unprocessed_tasks.remove(task)
                    end_searching_time += task.WCET
                    searching_deadline = task.deadline() if searching_deadline == None or task.deadline() < searching_deadline else searching_deadline

                else:
                    break
            
            while len(tasks_in_progress):
                frequency_decreasing_coefficient = (end_searching_time - self.time) / (searching_deadline - self.time)
                cpu.frequency = cpu.GetFrequency(frequency_decreasing_coefficient)
                # cpu.queue.append(copy.copy(tasks_in_progress[0]))
                CPU.Simple_Queue.append(copy.copy(tasks_in_progress[0]))
                cpu.LOG("Start calculating")
                
                tasks_in_progress[0].arrival_time = self.time
                tasks_in_progress[0].execution_frequency = cpu.frequency
                self.time += tasks_in_progress[0].AET / cpu.frequency
                cpu.energy_consumption += cpu.Energy_func(tasks_in_progress[0].AET)             
                # del cpu.queue[-1]
                # cpu.queue.append(copy.copy(tasks_in_progress[0]))
                del cpu.queue[-1]
                cpu.queue.append(copy.copy(tasks_in_progress[0]))
                del tasks_in_progress[0]
                cpu.LOG("Stop calculating", _ET="AET")


            cpu.frequency = sorted(cpu.freq_energy.keys())[0]
            if unprocessed_tasks:
                cpu.LOG("Waiting the next task")
                self.time = end_searching_time = unprocessed_tasks[0].arrival_time
                searching_deadline = None
            else:
                cpu.LOG("Waiting for the Period")
                cpu.energy_consumption += cpu.Energy_func(searching_deadline - self.time)
                self.time = searching_deadline
                cpu.LOG("Final schedule for period")

        print(*self.logs, sep='\n')