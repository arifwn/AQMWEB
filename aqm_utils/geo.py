
from aqm_utils import utm

def process_domain_data(domain_data_list, lat, lon, dx, dy):
    '''
    '''
    zone, hem = utm.get_zone_hem(lat, lon)
    base_easting, base_northing = utm.convert_to_utm(lat, lon)
    
    for domain in domain_data_list:
        print 'processing domain', domain['domain_id']
        w = domain['e_we'] - 1
        h = domain['e_sn'] - 1
        
        if domain['domain_id'] == 0:
            domain['dx'] = dx
            domain['dy'] = dy
            domain['base_easting'] = base_easting - (w / 2) * domain['dx']
            domain['base_northing'] = base_northing - (h / 2) * domain['dy']
        else:
            parent = domain_data_list[domain['parent_id']]
            domain['dx'] = parent['dx'] / domain['parent_grid_ratio']
            domain['dy'] = parent['dy'] / domain['parent_grid_ratio']
            start_x = domain['i_parent_start'] * parent['dx']
            start_y = domain['j_parent_start'] * parent['dy']
            domain['base_easting'] = parent['base_easting'] + start_x
            domain['base_northing'] = parent['base_northing'] + start_y
        
        lower_easting = domain['base_easting']
        lower_northing = domain['base_northing']
        lower_lat, lower_lon = utm.convert_to_latlon(lower_easting, lower_northing, zone, hem)
        
        upper_easting = domain['base_easting'] + w * domain['dx']
        upper_northing = domain['base_northing'] + h * domain['dy']
        upper_lat, upper_lon = utm.convert_to_latlon(upper_easting, upper_northing, zone, hem)
        
        domain['lower_lat'] = lower_lat
        domain['lower_lon'] = lower_lon
        domain['upper_lat'] = upper_lat
        domain['upper_lon'] = upper_lon
    
    return domain_data_list
