'''
Created on Nov 18, 2011

@author: Arif
'''
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404

from aqm_utils.server import rpc_client


@login_required
def test_plot(request):
    import matplotlib
    from mpl_toolkits.basemap import Basemap
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    
    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # lat_ts is the latitude of true scale.
    # resolution = 'c' means use crude resolution coastlines.
    
#    #mercator
#    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
    

    m = Basemap(width=36000000,height=27000000,rsphere=(6378137.00,6356752.3142),
                resolution='l',area_thresh=1000.,projection='lcc',
                lat_1=30.,lat_0=0.,lon_0=0.)
    
    fig = Figure()
    canvas = FigureCanvas(fig)
    m.ax = fig.add_axes([0, 0, 1, 1])
    
#    m.bluemarble(scale=0.5)
    m.drawcoastlines()
    m.drawmapboundary(fill_color='aqua') 
    m.fillcontinents(color='coral',lake_color='aqua')
    m.drawparallels(np.arange(-90.,91.,30.))
    m.drawmeridians(np.arange(-180.,181.,60.))
    
    response = HttpResponse(content_type='image/png')
    canvas.print_figure(response, dpi=100)
    return response

@login_required
def mercator(request):
    import matplotlib
    from mpl_toolkits.basemap import Basemap
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    
    upper_lat = float(request.GET.get('upper_lat', 20))
    upper_lon = float(request.GET.get('upper_lon', 145))
    lower_lat = float(request.GET.get('lower_lat',-20))
    lower_lon = float(request.GET.get('lower_lon',90))
    true_lat = float(request.GET.get('true_lat',5))
    
    draw_ref_point = False
    try:
        ref_lat = float(request.GET.get('ref_lat'))
        ref_lon = float(request.GET.get('ref_lon'))
        draw_ref_point = True
    except:
        pass
    
    m = Basemap(projection='merc',llcrnrlat=lower_lat,urcrnrlat=upper_lat,
                llcrnrlon=lower_lon,urcrnrlon=upper_lon,lat_ts=true_lat,
                resolution=None)
    
    fig = Figure()
    canvas = FigureCanvas(fig)
    m.ax = fig.add_axes([0.01,0.01,0.98,0.98])
    
#    m.drawcoastlines()
#    m.drawmapboundary(fill_color='aqua') 
#    m.fillcontinents(color='coral',lake_color='aqua')
#    m.etopo()
    m.drawlsmask(land_color='gray',ocean_color='white',lakes=True)
    m.drawparallels(np.arange(-90.,91.,30.), color='black')
    m.drawmeridians(np.arange(-180.,181.,60.), color='black')
    
    if draw_ref_point:
        x, y = m(ref_lon, ref_lat)
        m.plot(x, y, 'ro')
    
    response = HttpResponse(content_type='image/png')
    canvas.print_figure(response, dpi=80)
    return response

@login_required
def lambert_conformal(request):
    import matplotlib
    from mpl_toolkits.basemap import Basemap
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    
    width = float(request.GET.get('width', 6000000))
    height = float(request.GET.get('height', 4500000))
    lat = float(request.GET.get('lat',-7))
    lon = float(request.GET.get('lon',107))
    true_lat1 = float(request.GET.get('true_lat1',5))
    true_lat2 = float(request.GET.get('true_lat2',5))
    
    m = Basemap(width=width,height=height,
            rsphere=(6378137.00,6356752.3142),\
            resolution=None,projection='lcc',\
            lat_1=true_lat1,lat_2=true_lat2,lat_0=lat,lon_0=lon)
    
    fig = Figure()
    canvas = FigureCanvas(fig)
    m.ax = fig.add_axes([0, 0, 1, 1])
    
    m.drawlsmask(land_color='gray',ocean_color='white',lakes=True)
    m.drawparallels(np.arange(-90.,91.,30.), color='black')
    m.drawmeridians(np.arange(-180.,181.,60.), color='black')
    
    x, y = m(lon, lat)
    m.plot(x, y, 'ro')
    
    response = HttpResponse(content_type='image/png')
    canvas.print_figure(response, dpi=100)
    return response

@login_required
def wrf_domain_map(request, setting_id):
    from wrf.models import Setting
    
    try:
        setting = Setting.objects.get(id=setting_id)
    except Setting.DoesNotExist:
        raise Http404
    
    import matplotlib
    from mpl_toolkits.basemap import Basemap
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.patches import Polygon
    
    from aqm_utils.geo import process_domain_data
    
    dx = setting.dx
    dy = setting.dy
    
    ref_lat = setting.get_wps_namelist_data('geogrid', 'ref_lat', 0)
    ref_lon = setting.get_wps_namelist_data('geogrid', 'ref_lon', 0)
    domains = setting.get_all_domain()
    domains = process_domain_data(domains, ref_lat, ref_lon, dx, dy)
    
    upper_lat = ref_lat + 20
    upper_lon = ref_lon + 27
    lower_lat = ref_lat - 20
    lower_lon = ref_lon - 27
    
    try:
        domain = domains[0]
        upper_lat = domain['upper_lat'] + 2
        upper_lon = domain['upper_lon'] + 2
        lower_lat = domain['lower_lat'] - 2
        lower_lon = domain['lower_lon'] - 2
    except:
        pass
    
    true_lat = setting.get_wps_namelist_data('geogrid', 'truelat1', 0)
    
    m = Basemap(projection='merc',llcrnrlat=lower_lat,urcrnrlat=upper_lat,
                llcrnrlon=lower_lon,urcrnrlon=upper_lon,lat_ts=true_lat,
                resolution='l')
    
    fig = Figure()
    canvas = FigureCanvas(fig)
    m.ax = fig.add_axes([0.01,0.01,0.98,0.98])
    
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm', 'y',
                  'b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm', 'y']
    
    for domain in domains:
        print repr(domain)
        x1, y1 = m(domain['lower_lon'], domain['lower_lat'])
        x2, y2 = m(domain['lower_lon'], domain['upper_lat'])
        x3, y3 = m(domain['upper_lon'], domain['upper_lat'])
        x4, y4 = m(domain['upper_lon'], domain['lower_lat'])
        p = Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)],facecolor=color_list[domain['domain_id']],edgecolor='white',alpha=0.333,linewidth=1)
        m.ax.add_patch(p)
    
    #m.drawlsmask(land_color='gray',ocean_color='white',lakes=True)
    #m.drawparallels(np.arange(-90.,91.,30.), color='black')
    #m.drawmeridians(np.arange(-180.,181.,60.), color='black')
    
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    
    x, y = m(ref_lon, ref_lat)
    m.plot(x, y, 'ro')
    
    response = HttpResponse(content_type='image/png')
    canvas.print_figure(response, dpi=100)
    return response

@login_required
def grads_wrf_plot(request, server_id, envid):
    f = request.GET.get('f')
    if f is None:
        raise Http404
    
    c = rpc_client(server_id)
    if c is None:
        raise Http404
    
    binary_data = c.filesystem.read(envid, f)
    if binary_data is None:
        raise Http404
    
    response = HttpResponse(content_type='image/png')
    response.write(binary_data.data)
    return response
    
    
    