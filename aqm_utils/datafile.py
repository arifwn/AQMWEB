'''
Created on Jan 6, 2012

@author: arif
'''
from openpyxl.reader.excel import load_workbook
import logging

def get_excel_worksheets(path):
    '''return a dict containing excel sheet name as list'''
    logging.debug('Opening %s' % path)
    try:
        workbook = load_workbook(path)
        workbook_ok = True
    except Exception as ex:
        logging.exception(ex)
        workbook_ok = False
    
    if workbook_ok:
        return workbook.get_sheet_names()
    else:
        return None
    
def test():
    return get_excel_worksheets('media/test_data/emission_data/grid_marsel.xlsx')
