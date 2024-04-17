from classes import Task, BaseAlgo, CPU, states, DPM
from math import gcd
import copy

class DVS_DPM(BaseAlgo):
    def Run(self, cpu: CPU, tasks: list[Task]):
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

        print(cpu.QueueStrBase())
        # print(sum_of_exec)
        tasks = copy.deepcopy(cpu.queue)
        cpu.queue = []
        # tasks = sorted(tasks, key=lambda x: (x.arrival_time, x.arrival_time + x.period))
        logs = []

        logs.append(cpu.LOG("Start work"))

        end_searching_time = cpu.time = 0
        searching_deadline = None
        unprocessed_tasks = copy.deepcopy(tasks)
        tasks_in_progress = []
        
        while len(unprocessed_tasks):
            print(f"COUNT OF TASKS {len(unprocessed_tasks)}")
            # for task in unprocessed_tasks:
            #     if cpu.time <= task.arrival_time <= end_searching_time:
            #         tasks_in_progress.append(copy.copy(task))
            #         end_searching_time += task.WCET
            #         searching_deadline = task.deadline() if searching_deadline == None or task.deadline() < searching_deadline else searching_deadline
            #         unprocessed_tasks.remove(task)

            #     else:
            #         break
            uncorrect_tasks = []
            while (unprocessed_tasks and 
                    cpu.time <= unprocessed_tasks[0].arrival_time <= end_searching_time):
                print('FIND ONE')
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

            DPM_cpu = copy.deepcopy(cpu)
            DPM_tasks_in_progress = copy.deepcopy(tasks_in_progress)
            need_to_compare = True

            logs.append(DPM_cpu.LOG("===========DPM=============="))
            task_border = unprocessed_tasks[0].arrival_time if len(unprocessed_tasks) else searching_deadline
            tails = []
            for task in DPM_tasks_in_progress[::-1]:
                tail = min(task_border, task.deadline())
                task.arrival_time = tail - task.AET
                task_border = task.arrival_time
                tails.append(tail)

            for task in DPM_tasks_in_progress:
                if tails[-1] - DPM_cpu.time - states.time_to_set['ACTIVE']['TO_SLEEP'] - states.time_to_set['SLEEP']['TO_ACTIVE'] >= task.AET:
                    sleeping_time = tails[-1] - DPM_cpu.time - states.time_to_set['ACTIVE']['TO_SLEEP'] - states.time_to_set['SLEEP']['TO_ACTIVE'] - task.AET

                    logs.append(DPM_cpu.LOG("Use sleep mode"))
                    
                    DPM_cpu.energy_consumption += states.energy_to_set['ACTIVE']['TO_SLEEP']
                    DPM_cpu.DPM = DPM('SLEEP')
                    DPM_cpu.queue.append(f"ACTIVE->SLEEP: {DPM_cpu.time}->{DPM_cpu.time + states.time_to_set['ACTIVE']['TO_SLEEP']}")
                    DPM_cpu.time += states.time_to_set['ACTIVE']['TO_SLEEP']
                    logs.append(DPM_cpu.LOG("Set sleep mode"))

                    DPM_cpu.queue.append(f'SLEEP MODE: {DPM_cpu.time}->{DPM_cpu.time + sleeping_time}')
                    DPM_cpu.time += sleeping_time
                    DPM_cpu.energy_consumption += sleeping_time * states.energy_consumption['SLEEP']
                    logs.append(DPM_cpu.LOG("Sleep mode"))

                    DPM_cpu.energy_consumption += states.energy_to_set['SLEEP']['TO_ACTIVE']
                    DPM_cpu.DPM = DPM('ACTIVE')
                    DPM_cpu.queue.append(f"SLEEP->ACTIVE: {DPM_cpu.time}->{DPM_cpu.time + states.time_to_set['SLEEP']['TO_ACTIVE']}")
                    DPM_cpu.time += states.time_to_set['SLEEP']['TO_ACTIVE']
                    logs.append(DPM_cpu.LOG("Set active mode"))

                    DPM_cpu.queue.append(copy.copy(DPM_tasks_in_progress[0]))
                    DPM_cpu.queue[-1].start_execution_time = DPM_cpu.time
                    DPM_cpu.queue[-1].execution_time = DPM_cpu.queue[-1].AET
                    DPM_cpu.time += DPM_cpu.queue[-1].execution_time
                    DPM_cpu.energy_consumption += states.energy_consumption['ACTIVE'] * DPM_cpu.queue[-1].execution_time
                    logs.append(DPM_cpu.LOG("Execute Task"))

                    tails.pop()
                
                elif tails[-1] - DPM_cpu.time - states.time_to_set['ACTIVE']['TO_IDLE'] - states.time_to_set['IDLE']['TO_ACTIVE'] >= task.AET:
                    idleing_time = tails[-1] - DPM_cpu.time - states.time_to_set['ACTIVE']['TO_IDLE'] - states.time_to_set['IDLE']['TO_ACTIVE'] - task.AET

                    logs.append(DPM_cpu.LOG("Use idle mode"))
                    
                    DPM_cpu.energy_consumption += states.energy_to_set['ACTIVE']['TO_IDLE']
                    DPM_cpu.DPM = DPM('IDLE')
                    DPM_cpu.queue.append(f"ACTIVE->IDLE: {DPM_cpu.time}->{DPM_cpu.time + states.time_to_set['ACTIVE']['TO_IDLE']}")
                    DPM_cpu.time += states.time_to_set['ACTIVE']['TO_IDLE']
                    logs.append(DPM_cpu.LOG("Set idle mode"))

                    DPM_cpu.queue.append(f'IDLE MODE: {DPM_cpu.time}->{DPM_cpu.time + idleing_time}')
                    DPM_cpu.time += idleing_time
                    DPM_cpu.energy_consumption += idleing_time * states.energy_consumption['IDLE']
                    logs.append(DPM_cpu.LOG("Idle mode"))

                    DPM_cpu.energy_consumption += states.energy_to_set['IDLE']['TO_ACTIVE']
                    DPM_cpu.DPM = DPM('ACTIVE')
                    DPM_cpu.queue.append(f"IDLE->ACTIVE: {DPM_cpu.time}->{DPM_cpu.time + states.time_to_set['IDLE']['TO_ACTIVE']}")
                    DPM_cpu.time += states.time_to_set['IDLE']['TO_ACTIVE']
                    logs.append(DPM_cpu.LOG("Set active mode"))

                    DPM_cpu.queue.append(copy.copy(DPM_tasks_in_progress[0]))
                    DPM_cpu.queue[-1].start_execution_time = DPM_cpu.time
                    DPM_cpu.queue[-1].execution_time = DPM_cpu.queue[-1].AET
                    DPM_cpu.time += DPM_cpu.queue[-1].execution_time
                    DPM_cpu.energy_consumption += states.energy_consumption['ACTIVE'] * DPM_cpu.queue[-1].execution_time
                    logs.append(DPM_cpu.LOG("Execute Task"))

                    tails.pop()
                
                else:
                    wait_time = tails[-1] - DPM_cpu.time - task.AET
                    
                    logs.append(DPM_cpu.LOG("Use active mode"))
                    
                    DPM_cpu.queue.append(f'ACTIVE MODE: {DPM_cpu.time}->{DPM_cpu.time + wait_time}')
                    DPM_cpu.time += wait_time
                    DPM_cpu.energy_consumption += wait_time * states.energy_consumption['ACTIVE']
                    logs.append(DPM_cpu.LOG("Active mode"))

                    DPM_cpu.queue.append(copy.copy(DPM_tasks_in_progress[0]))
                    del DPM_tasks_in_progress[0]
                    DPM_cpu.queue[-1].start_execution_time = DPM_cpu.time
                    DPM_cpu.queue[-1].execution_time = DPM_cpu.queue[-1].AET
                    print('~', DPM_cpu.queue[-1].execution_time, '~')
                    DPM_cpu.time += DPM_cpu.queue[-1].execution_time
                    DPM_cpu.energy_consumption += states.energy_consumption['ACTIVE'] * DPM_cpu.queue[-1].execution_time
                    logs.append(DPM_cpu.LOG("Execute Task"))

                    tails.pop()


            logs.append(cpu.LOG("===========DVS=============="))
            while len(tasks_in_progress):
                frequency_decreasing_coefficient = (end_searching_time - cpu.time) / (searching_deadline - cpu.time)
                cpu.frequency = cpu.GetFrequency(frequency_decreasing_coefficient)
                print(f"frequency for {len(tasks_in_progress)} tasks == {cpu.frequency}")
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
                cpu.queue.append(f"DVS WAIT: {cpu.time}->{unprocessed_tasks[0].arrival_time}")
                cpu.energy_consumption += cpu.Energy_func(unprocessed_tasks[0].arrival_time - cpu.time)
                cpu.time = end_searching_time = unprocessed_tasks[0].arrival_time
                searching_deadline = None
                logs.append(cpu.LOG("Schedule for block"))
            else:
                logs.append(cpu.LOG("Waiting for the Period"))
                cpu.queue.append(f"DVS WAIT: {cpu.time}->{searching_deadline}")
                cpu.energy_consumption += cpu.Energy_func(searching_deadline - cpu.time)
                cpu.time = searching_deadline
                logs.append(cpu.LOG("Schedule for period"))

            dpm = False
            if DPM_cpu.energy_consumption < cpu.energy_consumption:
                dpm = True
                cpu = copy.deepcopy(DPM_cpu)
            logs.append(cpu.LOG(f"USE {'DPM' * (dpm) + 'DVS' * (not dpm)} STRATEGY"))
            
        logs.append(cpu.LOG("Final schedule for period"))
        print(*logs, sep='\n')