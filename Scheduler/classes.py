class states:
    states = ['ACTIVE', 'IDLE', 'SLEEP']
    
    time_to_set = {
        'ACTIVE': [0, 0.5, 1],
        'IDLE': [0.5, 0, 0.5],
        'SLEEP': [1.5, 1, 0]
    }

    energy_consumption = {
        'ACTIVE': 40000,
        'IDLE': 15000,
        'SLEEP': 400
    }

    def __str__(self):
        result = []
        for state in states:
            result.append(f'state {state}: {self.energy_consumption[state]} points of energy per second')
            for state_to in states:
                result.append(f'from {state} to ACTIVE: {self.time_to_set[state][0]}')
                result.append(f'from {state} to IDLE: {self.time_to_set[state][1]}')
                result.append(f'from {state} to SLEEP: {self.time_to_set[state][2]}')
            result.append('\n')
        
        return '\n'.join(result)


    def set_time_to_set(state: str, value: list[float]):
        time_to_set[state] = value
    
    def set_energy_consumption(state: str, value):
        energy_consumption[state] = value


class BaseAlgo:
    time = 0
    logs = []

    def Run(self, cpu, tasks):
        pass

class Logger:
    def __init__(self, cpu, msg):
        self.time = time
        self.cpu = cpu
        self.msg = msg

    def __str__(self):
        return f'''
        Log time: {self.time}
        CPU:
            frequency: {self.cpu.frequency},
            Total consumption: {self.cpu.energy_consumption},
            DPM: {'absent' if self.cpu.DPM == None else {'state': self.cpu.DPM.state, 'E-consumption': self.cpu.DPM.energy_consumption}}
            queue: {cpu.queue}
        '''

class DPM:

    def __init__(self, state):
        self.state = state
        self.time_to_set = states.time_to_set[state]
        self.energy_consumption = states.energy_consumption[state]


class Task:
    def __init__(self, arrival_time, period, WCET, AET):
        self.arrival_time = arrival_time
        self.period = period
        self.WCET = WCET
        self.AET = AET


    # def __init__(self, task):
    #     self.arrival_time = task.arrival_time
    #     self.period = task.period
    #     self.WCET = task.WCET
    #     self.AET = task.AET

    def __str__(self):
        return f"({self.arrival_time}|{self.period}|{self.WCET}|{self.AET})"
    

class CPU:

    def __init__(self, set_of_frequencies, enegry_consumption_by_frequency, has_DPM=False):
        for key, value in zip(set_of_frequencies, enegry_consumption_by_frequency):
            self.freq_energy[key] = value
        self.frequency = self.freq_energy.keys()[-1]
        # self.set_of_frequencies = set_of_frequencies
        # self.enegry_consumption_by_frequency = enegry_consumption_by_frequency # alpha * C_L * V_dd^2

        self.energy_consumption = 0
        self.queue = []
        self.DPM = DPM('ACTIVE') if has_DPM else None

        self.algo = None
    
    def Energy_func(self, execution_time):
        return self.


    def QueueStr(self):
        for task in self.queue:
            print(task, end = ' ')

    def sort_push_back(self, item, key: callable):
        place = 0
        for i in range(len(self.queue), 0, -1):
            if key(self.queue[i-1]) < key(item):
                place = i
                break
        self.queue.insert(place, item)

    def LOG(msg):
        algo.logs.append(Logger(self, msg))
