from classes import Task, BaseAlgo, CPU
from math import gcd
import copy

class DVS(BaseAlgo):
    def Run(self, cpu: CPU, tasks: list[Task]):
        try:
            # create scm wcet schedule
            lcm = tasks[0].period
            for task in tasks:
                lcm = lcm * task.period // gcd(lcm, task.period)
            
            # sum_of_exec = 0
            for task in tasks:
                for i in range(0, lcm, task.period):
                    task.arrival_time = i
                    cpu.sort_push_back(copy.copy(task), key=lambda x: (x.arrival_time, x.arrival_time + x.period))
                    
                    # sum_of_exec += task.WCET

            print("DVS")
            print(cpu.QueueStrBase())
            # print(sum_of_exec)
            tasks = copy.deepcopy(cpu.queue)
            cpu.queue = []
            # tasks = sorted(tasks, key=lambda x: (x.arrival_time, x.arrival_time + x.period))
            logs = []

###############################################################
            with open('Results_param.out', 'a') as file:
                max_freq_consumption = 0
                for task in tasks:
                    max_freq_consumption +=cpu.Energy_func(task.AET)
                print(f'Max Frequency Schedule: {max_freq_consumption}', sep='\n', file=file)
            
###############################################################

            logs.append(cpu.LOG("Start work"))

            end_searching_time = cpu.time = 0
            searching_deadline = None
            unprocessed_tasks = copy.deepcopy(tasks)
            tasks_in_progress = []
            
            while len(unprocessed_tasks):
                uncorrect_tasks = []
                while (unprocessed_tasks and 
                        cpu.time <= unprocessed_tasks[0].arrival_time <= end_searching_time):
                    tasks_in_progress.append(copy.copy(unprocessed_tasks[0]))
                    if (searching_deadline == None or
                            unprocessed_tasks[0].deadline() < searching_deadline):
                        searching_deadline = unprocessed_tasks[0].deadline()
                    
                    if end_searching_time + unprocessed_tasks[0].WCET > searching_deadline:
                        uncorrect_tasks.append(tasks_in_progress.pop())
                    else:
                        end_searching_time += unprocessed_tasks[0].WCET
                    
                    del unprocessed_tasks[0]
                
                unprocessed_tasks = uncorrect_tasks + unprocessed_tasks
            
                while len(tasks_in_progress):
                    if (searching_deadline == cpu.time):
                        frequency_decreasing_coefficient = 1
                    else:
                        frequency_decreasing_coefficient = (end_searching_time - cpu.time) / (searching_deadline - cpu.time)
                    cpu.frequency = cpu.GetFrequency(frequency_decreasing_coefficient)
    
                    if cpu.frequency is None:
                        cpu.frequency = 1
                    cpu.queue.append(copy.copy(tasks_in_progress[0]))
                    del tasks_in_progress[0]

                    cpu.queue[-1].start_execution_time = cpu.time
                    cpu.queue[-1].execution_frequency = cpu.frequency
                    logs.append(cpu.LOG("Start calculating"))
                    
                    cpu.queue[-1].execution_time = cpu.queue[-1].AET / cpu.frequency
                    cpu.time += cpu.queue[-1].execution_time
                    cpu.energy_consumption += cpu.Energy_func(cpu.queue[-1].execution_time)             
                    logs.append(cpu.LOG("Stop calculating"))


                cpu.frequency = sorted(cpu.freq_energy.keys())[0]
                if len(unprocessed_tasks):
                    logs.append(cpu.LOG("Waiting the next task"))
                    cpu.energy_consumption += cpu.Energy_func(unprocessed_tasks[0].arrival_time - cpu.time)
                    cpu.time = end_searching_time = unprocessed_tasks[0].arrival_time
                    searching_deadline = None
                else:
                    logs.append(cpu.LOG("Waiting for the Period"))
                    cpu.energy_consumption += cpu.Energy_func(searching_deadline - cpu.time)
                    cpu.time = searching_deadline
                    logs.append(cpu.LOG("Final schedule for period"))


            with open('Results_param.out', 'a') as file:
                print(f'DVS: {cpu.energy_consumption}', sep='\n', file=file)
            
            with open('DVS_logs.out', 'a') as file:
                print(logs[-1], sep='\n', file=file)
                
        except Exception as e:
            with open('Results_param.out', 'a') as file:
                print(f'DVS: BROKEN', sep='\n', file=file)
            with open('DVS_logs.out', 'a') as file:
                print("BROKEN SCHEDULE", file=file)
                print(e, file=file)
                print(*logs, sep='\n', file=file)



        #     with open('Results.out', 'a') as file:
        #         print(f'DVS: {cpu.energy_consumption}', sep='\n', file=file)
            
        #     with open('DVS_logs.out', 'a') as file:
        #         print(logs[-1], sep='\n', file=file)
                
        # except Exception as e:
        #     with open('Results.out', 'a') as file:
        #         print(f'DVS: BROKEN', sep='\n', file=file)
        #     with open('DVS_logs.out', 'a') as file:
        #         print("BROKEN SCHEDULE", file=file)
        #         print(e, file=file)
        #         print(*logs, sep='\n', file=file)
