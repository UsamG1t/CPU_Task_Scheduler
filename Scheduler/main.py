import classes, copy
from Algorithms import DVS, DVS_Priority
import sys

if (sys.argv[1] and sys.argv[1] == '--test'):
    cpu1 = classes.CPU([0.25, 0.5, 1], [3, 5, 8], 0)
    cpu2 = classes.CPU([0.25, 0.5, 1], [3, 5, 8], 0)
    print(f'''
    frequency <-> energy consumption per second
          1.0 <-> 8
          0.5 <-> 5
          0.25 <-> 3
    CPU without DPM
    ''')
else:
    set_of_frequencies = eval(input("set_of_frequencies(list): "))
    enegry_consumption_by_frequency = eval(input("enegry_consumption_by_frequency(list): "))
    has_DPM = bool(input("has_DPM: "))

    cpu1 = classes.CPU(set_of_frequencies, enegry_consumption_by_frequency, has_DPM)
    cpu2 = copy.deepcopy(cpu1)

# if (has_DPM):
#     print(cpu.dpm)
#     change = bool(input("Change? (1/0): "))
#     # if (change):
#     # /**/

count_of_tasks = int(input("count_of_tasks: "))
tasks = []
for i in range(count_of_tasks):
    arrival_time, period, wcet, aet = eval(input(f"Task {i}: arrival_time, period, wcet, aet: "))
    tasks.append(classes.Task(arrival_time, period, wcet, aet))
    tasks[-1].priority = i

# Algorithms.DVS.Run(cpu, tasks)
cpu1.algo = DVS.DVS()
cpu1.algo.Run(cpu1, tasks)
cpu2.algo = DVS_Priority.DVS_Priority()
cpu2.algo.Run(cpu2, tasks)