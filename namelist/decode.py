'''
Created on Nov 15, 2011

@author: Arif
'''
from cStringIO import StringIO as StringIO
import namelist

class NamelistParser(namelist.StateMachine):
    
    def __init__(self, string_data=None, file_data=None):
        
        namelist.StateMachine.__init__(self)
        
        if file_data is not None:
            self.namelist_data = file_data
        else:
            if string_data is None:
                self.namelist_data = StringIO()
            else:
                self.namelist_data = StringIO(string_data)
        
        self.parsed_data = {}
        self.current_section = ''
    
    def process(self, data):
        data = data.strip()
        if len(data) < 1:
            return
        
        if self.state == 'INIT':
            if data[0] == '&':
                self.current_section = data.replace('&', '')
                self.parsed_data[self.current_section] = dict()
                self.change_state('SECTION')
        
        if self.state == 'SECTION':
            if data[0] == '/':
                self.change_state('INIT')
            else:
                parsed_data = self.parse_config_line(data)
                if parsed_data is None:
                    return
                
                self.parsed_data[self.current_section][parsed_data[0]] = parsed_data[1]
    
    def parse_config_line(self, data):
        s = data.split('=')
        if len(s) < 2:
            return None
        config_name = s[0].strip()
        config_val = s[1].strip()
        config_vals = []
        
        val_list = config_val.split(',')
        for val in val_list:
            s_val = val.strip()
            if len(s_val) > 0:
                config_vals.append(namelist.get_value(s_val))
        
        return config_name, config_vals
        
    def decode(self):
        for line in self.namelist_data:
            self.process(line)
        

def decode_namelist(input_file):
    if isinstance(input_file, basestring):
        f = open(input_file)
    else:
        f = input_file
    parser = NamelistParser(file_data=f)
    parser.decode()
    return parser.parsed_data

def test():
    path = '../media/test_data/namelist.input'
    parsed_data = decode_namelist(path)
    for key in parsed_data:
        print '-------- %s -------' % key
        for key2 in parsed_data[key]:
            print key2,':', parsed_data[key][key2]

if __name__ == '__main__':
    test()    