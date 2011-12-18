'''
Created on Nov 15, 2011

@author: Arif
'''
from cStringIO import StringIO as StringIO
import namelist

class NamelistEncoder(namelist.StateMachine):
    
    def __init__(self, dict_data=None):
        namelist.StateMachine.__init__(self)
        
        if dict_data is None:
            self.source_data = dict()
        else:
            self.source_data = dict_data
        
        self.current_section = ''
        self.namelist_data = StringIO()
    
    def process(self, section_key=None, item_key=None, data=None):
        if section_key is None:
            self.change_state('INIT')
            self.namelist_data.write('/ \n \n')
            return
        
        if (item_key is None) or (data is None):
            return
        
        if self.state == 'INIT':
            self.change_state('SECTION')
            self.current_section = section_key
            self.namelist_data.write('&%s \n' % section_key)
        
        self.encode_line(item_key, data)
    
    def encode_line(self, item_key, data):
        line = '%-37s =' % item_key
        for item in data:
            s_data = ' %s,' % namelist.get_string(item)
            line += s_data
        line += '\n'
        self.namelist_data.write(line)
        
    def encode(self):
        for section_key in self.source_data:
            for item_key in self.source_data[section_key]:
                data = self.source_data[section_key][item_key]
                self.process(section_key, item_key, data)
            self.process()

def encode_namelist(data):
    encoder = NamelistEncoder(data)
    encoder.encode()
    return encoder.namelist_data.getvalue()
    
def test():
    from namelist.decode import decode_namelist
    
    path = '../media/test_data/namelist.input'
    print path
    parsed_data = decode_namelist(path)
    
    import json
    js_string = json.dumps(parsed_data)
    parsed_data = json.loads(js_string)
    
    print encode_namelist(parsed_data)
    
if __name__ == '__main__':
    test()
    