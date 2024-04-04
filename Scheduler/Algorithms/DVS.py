from classes import Task, BaseAlgo
from math import gcd

class DVS(BaseAlgo):
    def Run(self, cpu, tasks: list[Task]):
        # create scm wcet schedule
        lcm = tasks[0].period
        for task in tasks:
            lcm = lcm * task.period // gcd(lcm, task.period)
        
        sum_of_exec = 0
        for task in tasks:
            for i in range(0, lcm, task.period):
                cpu.sort_push_back(Task(i, task.period, task.WCET, task.AET), key=lambda x: (x.arrival_time, x.arrival_time + x.period))
                sum_of_exec += task.WCET
        cpu.QueueStr()
        print()
        print(sum_of_exec)
        
    cpu.LOG("Start work")

    
