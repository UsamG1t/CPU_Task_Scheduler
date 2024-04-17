import copy

class states:
    states = ['ACTIVE', 'IDLE', 'SLEEP']
    
    time_to_set = {
        'ACTIVE': {'TO_ACTIVE': 0, 'TO_IDLE': 0.5, 'TO_SLEEP': 1},
        'IDLE': {'TO_ACTIVE': 0.5, 'TO_IDLE': 0, 'TO_SLEEP': 0.5},
        'SLEEP': {'TO_ACTIVE': 1.5, 'TO_IDLE': 1, 'TO_SLEEP': 0}
    }

    energy_to_set = {
        'ACTIVE': {'TO_ACTIVE': 0, 'TO_IDLE': 15, 'TO_SLEEP': 12},
        'IDLE': {'TO_ACTIVE': 15, 'TO_IDLE': 0, 'TO_SLEEP': 6},
        'SLEEP': {'TO_ACTIVE': 8, 'TO_IDLE': 4, 'TO_SLEEP': 0}
    }

    energy_consumption = {
        'ACTIVE': 40,
        'IDLE': 20,
        'SLEEP': 4
    }

    def __str__(self):
        result = []
        for state in self.states:
            result.append(f'state {state}: {self.energy_consumption[state]} points of energy per second')
            result.append(f'from {state} to ACTIVE: {self.time_to_set[state]["TO_ACTIVE"]}')
            result.append(f'from {state} to IDLE: {self.time_to_set[state]["TO_IDLE"]}')
            result.append(f'from {state} to SLEEP: {self.time_to_set[state]["TO_SLEEP"]}')
            result.append('\n')
        
        return '\n'.join(result)


    # def set_time_to_set(state: str, value: list[float]):
    #     states.time_to_set[state] = value
    
    # def set_energy_consumption(state: str, value):
    #     states.energy_consumption[state] = value


class BaseAlgo:
    time = 0
    logs = []

    def Run(self, cpu, tasks):
        pass


class DPM:

    def __init__(self, state):
        self.state = state
        self.time_to_set = states.time_to_set[state]
        self.energy_consumption = states.energy_consumption[state]


class Task:
    NUM = 0
    def __init__(self, arrival_time, period, WCET, AET):
        self.num = Task.NUM
        Task.NUM += 1
        self.arrival_time = arrival_time
        self.period = period
        self.WCET = WCET
        self.AET = AET
        self.execution_frequency = None
        self.start_execution_time = None
        self.execution_time = None
        self.priority = None
        
    def deadline(self):
        return self.arrival_time + self.period

    def __repr__(self):
        finish_execution_time = None if self.execution_time is None else self.start_execution_time + self.execution_time
        return f"({self.num}: Freq {self.execution_frequency} time {self.start_execution_time}->{finish_execution_time})"

    def __str__(self):
        return f"({self.arrival_time}|{self.period}|{self.WCET}|{self.AET})"
    
class CPU:
    Simple_Queue = []

    def __init__(self, set_of_frequencies, enegry_consumption_by_frequency, has_DPM=False):

        self.freq_energy = {}
        for key, value in zip(set_of_frequencies, enegry_consumption_by_frequency):
            self.freq_energy[key] = value # alpha * C_L * V_dd^2

        self.frequency = sorted(self.freq_energy.keys())[-1]
        self.energy_consumption = 0
        self.queue = []
        self.DPM = DPM('ACTIVE') if has_DPM else None

        self.algo = None
        self.time = 0

    def Energy_func(self, execution_time):
        return self.freq_energy[self.frequency] * execution_time

    def GetFrequency(self, alpha):
        for frequency in sorted(self.freq_energy.keys()):
            if frequency >= alpha:
                return frequency

    def QueueStr(self):
        return ' '.join(task.__repr__() for task in self.queue)

    def QueueStrBase(self):
        return ' '.join(task.__str__() for task in self.queue)

    def sort_push_back(self, item, key: callable):
        place = 0
        for i in range(len(self.queue), 0, -1):
            if key(self.queue[i-1]) < key(item):
                place = i
                break
        self.queue.insert(place, item)

    def LOG(self, msg):
        return f'''
        Log time: {self.time}
        CPU:
            frequency: {self.frequency},
            Total consumption: {self.energy_consumption},
            DPM: {'absent' if self.DPM == None else {'state': self.DPM.state, 'E-consumption': self.DPM.energy_consumption}}
            queue: {self.QueueStr()}

        Message: {msg}
        '''
    
# class Logger:
#     def __init__(self, cpu: CPU, msg, _ET='WCET'):
#         self.time = cpu.algo.time
#         self.cpu = cpu
#         self.msg = msg

#         self._ET = _ET

#     def __str__(self):
#         return f'''
#         Log time: {self.time}
#         CPU:
#             frequency: {self.cpu.frequency},
#             Total consumption: {self.cpu.energy_consumption},
#             DPM: {'absent' if self.cpu.DPM == None else {'state': self.cpu.DPM.state, 'E-consumption': self.cpu.DPM.energy_consumption}}
#             queue: {self.cpu.QueueStr(LOG=True, _ET=self._ET)}

#         Message: {self.msg}
#         '''
