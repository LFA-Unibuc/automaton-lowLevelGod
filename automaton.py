from dbus import ValidationException


class Automaton():
    
    def __init__(self, config_file):
        self.config_file = config_file
        file = open(self.config_file)
        d = {}
        current_set = None
        for line in file.readlines():
            line = line.strip().rstrip()
            if line.startswith("#") == False:
                if line.lower() != "End".lower():
                    if ':' in line:
                        current_set = line.split(":")[0].rstrip()
                        if current_set == 'Transitions':
                            d[current_set] = {}
                        else:
                            d[current_set] = []
                    else:
                        line = tuple([x.strip().rstrip() for x in line.split(",")])
                        if current_set == 'Transitions':
                            if line[0] in d[current_set]:
                                if line[1] in d[current_set][line[0]]:
                                    if line[2] not in d[current_set][line[0]][line[1]]:
                                        d[current_set][line[0]][line[1]].append(line[2])
                                else:
                                    d[current_set][line[0]][line[1]] = []
                            else:
                                d[current_set][line[0]] = {line[1] : [line[2], ]}
                        else:
                            d[current_set].append(line)
        d['fstates'] = []
        d['sstates'] = []
        for state in d['States']:
            for s in state[1:]:
                if s == 'F':
                    d["fstates"].append(state[0])
                elif s == 'S':
                    d["sstates"].append(state[0])
        d['Sigma'] = [x[0] for x in d['Sigma']]
        d['States'] = [x[0] for x in d['States']]
        file.close()
        self.data = d
        print(d)
        print("Hi, I'm an automaton!")

    def validate(self):
        d = self.data
        if len(d['sstates']) > 1:
            raise ValidationException("Only one starting state allowed !")
        for t in d['Transitions'].keys():
            all_states = [x for x in d['States']]
            all_words = [x for x in d['Sigma']]
            lhs = t
            mid = None
            for x in d['Transitions'][t]:
                mid = x
            rhs = None
            if mid != None:
                for x in d['Transitions'][t][mid]:
                    rhs = x
            if lhs not in all_states or mid == None or rhs == None:
                raise ValidationException("Invalid transition")
        return True

    def accepts_input(self, input_str):
        """Return a Boolean

        Returns True if the input is accepted,
        and it returns False if the input is rejected.
        """
        pass

    def read_input(self, input_str):
        """Return the automaton's final configuration
        
        If the input is rejected, the method raises a
        RejectionException.
        """
        pass
    
if __name__ == "__main__":
    a = Automaton('input.txt')
    print(a.validate())

