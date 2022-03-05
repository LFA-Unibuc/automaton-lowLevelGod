from dbus import ValidationException


class Automaton():
    
    def __init__(self, config_file):
        self.config_file = config_file
        file = open(self.config_file)
        d = {}
        current_set = ""
        for line in file.readlines():
            line = line.rstrip().strip()
            if '#' not in line:
                if ':' in line:
                    line = line.split(":", maxsplit=1)[0].rstrip()
                    d[line] = []
                    current_set = line
                else:
                    if line != "End":
                        tple = []
                        for x in line.split(","):
                            tple.append(x.rstrip().strip())
                        tple = tuple(tple)
                        d[current_set].append(tple)
        file.close()
        self.data = d
        print("Hi, I'm an automaton!")

    def validate(self):
        d = self.data
        start_states = sum(1 for x in d["States"] if len(x) > 1 if x[1] == 'S')
        if start_states > 1:
            raise ValidationException("Only one starting state allowed !")
        for t in d['Transitions']:
            all_states = [x[0] for x in d['States']]
            all_words = [x[0] for x in d['Sigma']]
            if t[0] not in all_states or t[1] not in all_words or t[2] not in all_states:
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

