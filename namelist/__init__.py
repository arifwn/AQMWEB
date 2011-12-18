
class StateMachine():
    def __init__(self):
        self.state = 'INIT'
    
    def change_state(self, state):
        self.state = state

def get_value(s_input):
    if s_input == '.true.':
        o_val = True
    elif s_input == '.false.':
        o_val = False
    else:
        try_float = False
        try:
            o_val = int(s_input)
        except ValueError:
            try_float = True
        
        if try_float:
            try:
                o_val = float(s_input)
            except ValueError:
                o_val = s_input
                
    return o_val

def get_string(value):
    if isinstance(value, float):
        s_out = '%.6g' % value
        s_out = s_out.replace('+', '')
        if (s_out.find('.') == -1) and (s_out.find('e') == -1):
            s_out += '.'
    elif isinstance(value, bool):
        if value:
            s_out = '.true.'
        else:
            s_out = '.false.'
    elif isinstance(value, int):
        s_out = '%s' % value
    else:
        s_out = '%s' % value
    return s_out

if __name__ == '__main__':
    print '=== get_string ==='
    print 1.0, get_string(1.0), get_value('1.')
    print 1.234, get_string(1.234), get_value('1.234')
    print 10000000.0, get_string(10000000.0), get_value('1e7')
    print 1, get_string(1), get_value('1')
    print True, get_string(True), get_value('.true.')
    print False, get_string(False), get_value('.false.')
    