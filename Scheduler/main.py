import classes, copy
from Algorithms import DVS, DVS_Priority, DVS_DPM
import sys

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
        
        count_of_tasks = int(file.readline())
        tasks = []
        for i in range(count_of_tasks):
            arrival_time, period, wcet, aet = eval(file.readline())
            tasks.append(classes.Task(arrival_time, period, wcet, aet))
            tasks[-1].priority = i

else:
    set_of_frequencies = eval(input("set_of_frequencies(list): "))
    enegry_consumption_by_frequency = eval(input("enegry_consumption_by_frequency(list): "))
    has_DPM = bool(input("has_DPM: "))

    cpu1 = classes.CPU(set_of_frequencies, enegry_consumption_by_frequency, has_DPM)
    cpu2 = copy.deepcopy(cpu1)

    count_of_tasks = int(input("count_of_tasks: "))
    tasks = []
    for i in range(count_of_tasks):
        arrival_time, period, wcet, aet = eval(input(f"Task {i}: arrival_time, period, wcet, aet: "))
        tasks.append(classes.Task(arrival_time, period, wcet, aet))
        tasks[-1].priority = i

cpu1.algo = DVS.DVS()
cpu1.algo.Run(cpu1, copy.deepcopy(tasks))
cpu2.algo = DVS_Priority.DVS_Priority()
cpu2.algo.Run(cpu2, copy.deepcopy(tasks))
cpu3.algo = DVS_DPM.DVS_DPM()
cpu3.algo.Run(cpu3, copy.deepcopy(tasks))

