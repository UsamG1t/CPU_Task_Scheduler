from classes import Task, BaseAlgo, CPU
from math import gcd
import copy

class DVS_Priority(BaseAlgo):
    def Run(self, cpu: CPU, tasks: list[Task]):
        logs = []
        try:
            # create scm wcet schedule
            lcm = tasks[0].period
            for task in tasks:
                lcm = lcm * task.period // gcd(lcm, task.period)
            
            # sum_of_exec = 0
            for task in tasks:
                for i in range(0, lcm, task.period):
                    task.arrival_time = i
                    cpu.sort_push_back(copy.copy(task), key=lambda x: (x.arrival_time, x.priority, x.arrival_time + x.period))
                    
                    # sum_of_exec += task.WCET
            print(cpu.QueueStrBase())
            i = 0
            length = len(cpu.queue)
            while i < length - 1:
                interruption_search_start = cpu.queue[i].arrival_time + 1
                preinterrupt_time_end = None
                interrupt_shift = 0
                interruption_search_end = cpu.queue[i].deadline()

                inter_task = i + 1
                current_wcet = cpu.queue[i].WCET - 1
                current_aet = cpu.queue[i].AET - 1
                current_time = interruption_search_start
                while (current_wcet > 0 and current_time < interruption_search_end):
                    if cpu.queue[inter_task].arrival_time == current_time and cpu.queue[inter_task].priority < cpu.queue[i].priority:
                        # print(f"FIND on time {current_time}")
                        if preinterrupt_time_end is None:
                            preinterrupt_time_end = current_time
                        interrupt_shift += cpu.queue[inter_task].WCET
                        inter_task += 1
                        if inter_task == length:
                            break
                        current_time -= 1
                    current_time += 1
                    current_wcet -= 1
                    current_aet -= 1

                if preinterrupt_time_end is not None:
                    if (cpu.queue[i].arrival_time + cpu.queue[i].AET - preinterrupt_time_end > 0):
                        cpu.sort_push_back(Task(arrival_time=preinterrupt_time_end + interrupt_shift,
                                                period=cpu.queue[i].period,
                                                WCET=current_wcet,
                                                AET=max(current_aet, 0)),
                                            key=lambda x: (x.arrival_time, x.priority, x.arrival_time + x.period))
                    cpu.queue[i].WCET -= current_wcet
                    cpu.queue[i].AET -= max(current_aet, 0)
                
                length = len(cpu.queue)
                i += 1

            print(cpu.QueueStrBase())
            tasks = copy.deepcopy(cpu.queue)
            cpu.queue = []

            logs.append(cpu.LOG("Start work"))

            end_searching_time = cpu.time = 0
            searching_deadline = None
            unprocessed_tasks = copy.deepcopy(tasks)
            tasks_in_progress = []
            
            while len(unprocessed_tasks):
                # print(f"COUNT OF TASKS {len(unprocessed_tasks)}")
            #   
                for task in unprocessed_tasks:
                    if cpu.time <= task.arrival_time <= end_searching_time:
                        tasks_in_progress.append(copy.copy(task))
                        end_searching_time += task.WCET
                        searching_deadline = task.deadline() if searching_deadline == None or task.deadline() < searching_deadline else searching_deadline
                        unprocessed_tasks.remove(task)

                    else:
                        break
            # 
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

            with open('Results.out', 'a') as file:
                print(f'DVS_Priority: {cpu.energy_consumption}', sep='\n', file=file)

            with open('DVS_Priority_logs.out', 'a') as file:
                print(logs[-1], sep='\n', file=file)

        except Exception as e:
            with open('Results.out', 'a') as file:
                print(f'DVS_Priority: BROKEN', sep='\n', file=file)
            with open('DVS_Priority_logs.out', 'a') as file:
                print("BROKEN SCHEDULE", file=file)
                print(e, file=file)
                # print(*logs, sep='\n', file=file)