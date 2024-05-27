import classes, copy
from Algorithms import DVS, DVS_Priority, DVS_DPM, DPM
import sys

def Percentize(tasks: list[classes.Task], percent: float, N: float) -> list[classes.Task]:
    for task in tasks:
        task.AET = round(task.AET / N * percent, 2)
        task.WCET = round(task.WCET / N * percent, 2)
    return tasks

if (sys.argv[1] and sys.argv[1] == '--test'):
    cpu1 = classes.CPU([0.25, 0.5, 1], [15, 25, 40], 0)
    cpu2 = classes.CPU([0.25, 0.5, 1], [15, 25, 40], 0)
    cpu3 = classes.CPU([0.25, 0.5, 1], [15, 25, 40], 1)
    print(f'''
    frequency <-> energy consumption per second
          1.0 <-> 8
          0.5 <-> 5
          0.25 <-> 3
    CPU without DPM
    
    CPU with DPM:
        {classes.states().__str__()}
    ''')
    count_of_tasks = int(input("count_of_tasks: "))
    tasks = []
    for i in range(count_of_tasks):
        arrival_time, period, wcet, aet = eval(input(f"Task {i}: arrival_time, period, wcet, aet: "))
        tasks.append(classes.Task(arrival_time, period, wcet, aet))
        tasks[-1].priority = i

elif sys.argv[1] == '--file':
    with open(sys.argv[2], 'r') as file:
        set_of_frequencies = eval(file.readline())
        enegry_consumption_by_frequency = eval(file.readline())
        cpu1 = classes.CPU(set_of_frequencies=set_of_frequencies,
                           enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                           has_DPM=0)
        cpu2 = classes.CPU(set_of_frequencies=set_of_frequencies,
                           enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                           has_DPM=0)
        cpu3 = classes.CPU(set_of_frequencies=set_of_frequencies,
                           enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                           has_DPM=1)
        
        tasks = []
        count_of_tasks = int(file.readline())
        with open('Results.out', 'a') as res:
            print("~~~~~~~~", count_of_tasks, sep = '\n', file=res)

            for i in range(count_of_tasks):
                arrival_time, period, wcet, aet = eval(file.readline())
                print(arrival_time, period, wcet, aet, file=res)
                tasks.append(classes.Task(arrival_time, period, wcet, aet))
                tasks[-1].priority = i

elif sys.argv[1] == 'Parametrize':
    with open('Parametrize.sch', 'r') as file:
        Info = eval(file.read())
    
    for DVS_param in range(2):
        for DPM_param in range(2, 4):
            for Task_set in range(6):

                set_of_frequencies = Info['DVS'][DVS_param]['set_of_frequencies']
                enegry_consumption_by_frequency = Info['DVS'][DVS_param]['enegry_consumption_by_frequency']
                enegry_consumption = Info['DPM'][DPM_param]['energy_consumption']
                energy_to_set = Info['DPM'][DPM_param]['energy_to_set']

                cpu1 = classes.CPU(set_of_frequencies=set_of_frequencies,
                                enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                                has_DPM=0)
                cpu2 = classes.CPU(set_of_frequencies=set_of_frequencies,
                                enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                                has_DPM=0)
                cpu3 = classes.CPU(set_of_frequencies=set_of_frequencies,
                                enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                                has_DPM=1)
                tasks = []
                count_of_tasks = len(Info['Set'][Task_set])
                

                with open('Results_param.out', 'a') as res:
                    print(f"DVS: {set_of_frequencies} <-> {enegry_consumption_by_frequency}", file=res)
                    print(enegry_consumption, file=res)
                    print(energy_to_set, file=res)
                    print("~~~~~~~~", count_of_tasks, sep = '\n', file=res)

                    for i in range(count_of_tasks):
                        arrival_time, period, wcet, aet = Info['Set'][Task_set][i]
                        print(arrival_time, period, wcet, aet, file=res)
                        tasks.append(classes.Task(arrival_time, period, wcet, aet))
                        tasks[-1].priority = i

                N = 0
                for task in tasks:
                    N += task.WCET / task.period
            
                for percent in [1, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]:
                    percent_tasks = Percentize(copy.deepcopy(tasks), percent, N)
                    with open('Results_param.out', 'a') as file:
                        print(f'{100*percent}%', ' ', sep='\n', file=file)

                    cpuA = copy.deepcopy(cpu1)
                    cpuA.algo = DVS.DVS()
                    cpuA.algo.Run(cpuA, copy.deepcopy(percent_tasks))
                    
                    cpuB = copy.deepcopy(cpu2)
                    cpuB.algo = DVS_Priority.DVS_Priority()
                    cpuB.algo.Run(cpuB, copy.deepcopy(percent_tasks))
                    
                    cpuC = copy.deepcopy(cpu3)
                    cpuC.algo = DVS_DPM.DVS_DPM()
                    cpuC.algo.Run(cpuC, copy.deepcopy(percent_tasks), enegry_consumption, energy_to_set)

elif sys.argv[1] == 'DPM_time':
    with open('Par.sch', 'r') as file:
        Info = eval(file.read())
    
    for DPM_param in range(7):

        set_of_frequencies = Info['DVS'][0]['set_of_frequencies']
        enegry_consumption_by_frequency = Info['DVS'][0]['enegry_consumption_by_frequency']
        enegry_consumption = Info['DPM'][DPM_param]['energy_consumption']
        energy_to_set = Info['DPM'][DPM_param]['energy_to_set']

        cpu1 = classes.CPU(set_of_frequencies=set_of_frequencies,
                        enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                        has_DPM=0)
        cpu2 = classes.CPU(set_of_frequencies=set_of_frequencies,
                        enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                        has_DPM=0)
        cpu3 = classes.CPU(set_of_frequencies=set_of_frequencies,
                        enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                        has_DPM=1)
        cpu4 = classes.CPU(set_of_frequencies=set_of_frequencies,
                        enegry_consumption_by_frequency=enegry_consumption_by_frequency,
                        has_DPM=1)
        
        tasks = []
        count_of_tasks = len(Info['Set'][0])
        

        with open('Results_param.out', 'a') as res:
            print(f"DVS: {set_of_frequencies} <-> {enegry_consumption_by_frequency}", file=res)
            print(enegry_consumption, file=res)
            print(energy_to_set, file=res)
            print("~~~~~~~~", count_of_tasks, sep = '\n', file=res)

            for i in range(count_of_tasks):
                arrival_time, period, wcet, aet = Info['Set'][0][i]
                print(arrival_time, period, wcet, aet, file=res)
                tasks.append(classes.Task(arrival_time, period, wcet, aet))
                tasks[-1].priority = i

        N = 0
        for task in tasks:
            N += task.WCET / task.period
    
        percent_tasks = Percentize(copy.deepcopy(tasks), 0.6, N)
        with open('Results_param.out', 'a') as file:
            print(f'60%, DPM #{DPM_param}', ' ', sep='\n', file=file)

        cpuA = copy.deepcopy(cpu1)
        cpuA.algo = DVS.DVS()
        cpuA.algo.Run(cpuA, copy.deepcopy(percent_tasks))
        
        cpuB = copy.deepcopy(cpu2)
        cpuB.algo = DVS_Priority.DVS_Priority()
        cpuB.algo.Run(cpuB, copy.deepcopy(percent_tasks))
        
        cpuC = copy.deepcopy(cpu3)
        cpuC.algo = DVS_DPM.DVS_DPM()
        cpuC.algo.Run(cpuC, copy.deepcopy(percent_tasks), enegry_consumption, energy_to_set)

        cpuD = copy.deepcopy(cpu4)
        cpuD.algo = DPM.DPM()
        cpuD.algo.Run(cpuD, copy.deepcopy(percent_tasks), enegry_consumption, energy_to_set)


# else:
#     set_of_frequencies = eval(input("set_of_frequencies(list): "))
#     enegry_consumption_by_frequency = eval(input("enegry_consumption_by_frequency(list): "))
#     has_DPM = bool(input("has_DPM: "))

#     cpu1 = classes.CPU(set_of_frequencies, enegry_consumption_by_frequency, has_DPM)
#     cpu2 = copy.deepcopy(cpu1)

#     count_of_tasks = int(input("count_of_tasks: "))
#     tasks = []
#     for i in range(count_of_tasks):
#         arrival_time, period, wcet, aet = eval(input(f"Task {i}: arrival_time, period, wcet, aet: "))
#         tasks.append(classes.Task(arrival_time, period, wcet, aet))
#         tasks[-1].priority = i


# for percent in [1, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]:
#     percent_tasks = Percentize(copy.deepcopy(tasks), percent)
#     with open('Results.out', 'a') as file:
#         print(f'{100*percent}%', ' ', sep='\n', file=file)

#     cpuA = copy.deepcopy(cpu1)
#     cpuA.algo = DVS.DVS()
#     cpuA.algo.Run(cpuA, copy.deepcopy(percent_tasks))
    
#     cpuB = copy.deepcopy(cpu2)
#     cpuB.algo = DVS_Priority.DVS_Priority()
#     cpuB.algo.Run(cpuB, copy.deepcopy(percent_tasks))
    
#     cpuC = copy.deepcopy(cpu3)
#     cpuC.algo = DVS_DPM.DVS_DPM()
#     cpuC.algo.Run(cpuC, copy.deepcopy(percent_tasks))

