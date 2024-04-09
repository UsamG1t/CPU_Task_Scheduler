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
        logs = []

        logs.append(cpu.LOG("Start work"))

        end_searching_time = cpu.time = 0
        searching_deadline = None
        unprocessed_tasks = copy.deepcopy(tasks)
        tasks_in_progress = []
        
        while len(unprocessed_tasks):
            print(f"COUNT OF TASKS {len(unprocessed_tasks)}")
            # for task in unprocessed_tasks:
            #     if self.time <= task.arrival_time <= end_searching_time:
            #         tasks_in_progress.append(copy.copy(task))
            #         end_searching_time += task.WCET
            #         searching_deadline = task.deadline() if searching_deadline == None or task.deadline() < searching_deadline else searching_deadline
            #         unprocessed_tasks.remove(task)

            #     else:
            #         break
            
            while (unprocessed_tasks and 
                    self.time <= unprocessed_tasks[0].arrival_time <= end_searching_time):
                print('FIND ONE')
                tasks_in_progress.append(copy.copy(unprocessed_tasks[0]))
                end_searching_time += unprocessed_tasks[0].WCET
                if (searching_deadline == None or
                        unprocessed_tasks[0].deadline() < searching_deadline):
                    searching_deadline = unprocessed_tasks[0].deadline()
                
                del unprocessed_tasks[0]
            
            while len(tasks_in_progress):
                frequency_decreasing_coefficient = (end_searching_time - self.time) / (searching_deadline - self.time)
                cpu.frequency = cpu.GetFrequency(frequency_decreasing_coefficient)
                cpu.queue.append(copy.copy(tasks_in_progress[0]))
                del tasks_in_progress[0]

                cpu.queue[-1].start_execution_time = cpu.time
                cpu.queue[-1].execution_frequency = cpu.frequency
                logs.append(cpu.LOG("Start calculating"))
                
                cpu.queue[-1].execution_time = cpu.queue[-1].AET / cpu.frequency
                self.time += cpu.queue[-1].execution_time
                cpu.energy_consumption += cpu.Energy_func(cpu.queue[-1].execution_time)             
                logs.append(cpu.LOG("Stop calculating"))


            cpu.frequency = sorted(cpu.freq_energy.keys())[0]
            if len(unprocessed_tasks):
                logs.append(cpu.LOG("Waiting the next task"))
                cpu.energy_consumption += cpu.Energy_func(unprocessed_tasks[0].arrival_time - self.time)
                self.time = end_searching_time = unprocessed_tasks[0].arrival_time
                searching_deadline = None
            else:
                logs.append(cpu.LOG("Waiting for the Period"))
                cpu.energy_consumption += cpu.Energy_func(searching_deadline - self.time)
                self.time = searching_deadline
                logs.append(cpu.LOG("Final schedule for period"))

        print(*logs, sep='\n')