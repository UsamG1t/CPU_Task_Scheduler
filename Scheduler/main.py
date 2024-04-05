import classes
from Algorithms import DVS
import sys

if (sys.argv[1] and sys.argv[1] == '--test'):
    cpu = classes.CPU([0.25, 0.5, 1], [3, 5, 8], 0)
else:
    set_of_frequencies = eval(input("set_of_frequencies(list): "))
    enegry_consumption_by_frequency = eval(input("enegry_consumption_by_frequency(list): "))
    has_DPM = bool(input("has_DPM: "))

    cpu = classes.CPU(set_of_frequencies, enegry_consumption_by_frequency, has_DPM)

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

# Algorithms.DVS.Run(cpu, tasks)
cpu.algo = DVS.DVS()
cpu.algo.Run(cpu, tasks)