                     # import_file.py
import pandas as pd
import re
from api import models
from pyproj import Proj, transform
import os

def get_decimal_degree(s):
    """ Convert ugly string to decimal degree
    Antea comes as Long: '6° 55\' 18.12588" E'
    """
    # Get floats
    pp = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    nn = [float(i) for i in pp]
    # make sure negative when west or south
    if s.lower()[-1] in ['w','s']:
        nn[0] = -abs(nn[0])
    return nn[0] + nn[1]/60 + nn[2]/(60*60)



def checkColumns(data):
    ''' Check height column, and find location

    Now works for Heiligerlee and Barradeel delivery formats 
    '''
    err = []
    cols = data.columns.values

    if 'Hgt_ruw' in cols:
        col_h = 'Hgt_ruw'
    else:
        col_h = None

    # Heiligerlee version
    if 'Long' in cols and 'Lat' in cols:
        lon = get_decimal_degree(data.Long[0])
        lat = get_decimal_degree(data.Lat[0])

    # Barradeel version  
    elif 'X' in cols and 'Y' in cols:
        x = data.X[0]
        y = data.Y[0]
        if y > 289000 and y < 629000 and x > -7000 and x < 300000:
            # Guess RD coordinates
            inProj = Proj(init='epsg:28992')
            outProj = Proj(init='epsg:4326')
            lat,lon = transform(inProj,outProj,x,y)

    else:
        lon,lat = None,None

    return col_h,lon,lat


# TODO Make read RD coordinates for BARRADEEL!

def import_xlsx(file_stored,name=None,filename=None,contributor=None):
    """ For now, assume that it is an Antea GPS file with proper columns
    """
    # file = 'data/AGBA4.xlsx'
    # name = None
    # contributor=None
    # file_stored=None

    print ('\n\n FILE ',filename)
    print ('\n\n STORED ',file_stored)
    print ('\n\n NAME ',name)
    print ('\n\n')


    if filename is None:
        filename = os.path.split(file_stored)[1]

    data = pd.read_excel(file_stored)
    data = data.set_index('Date_time')

    msg = [('filename',file_stored),('loc_name_provided',name)]

    col_h,lon,lat = checkColumns(data)
    if col_h is None:
        msg.append(('ERROR','No height column recognized'))
    if lon is None:
        msg.append(('ERROR','No coordinates recognized'))

    locs = models.Location.objects.all()
    # pick right location
    my_location=None
    for l in locs:
        if abs(l.lon - lon)<0.0001 and abs(l.lat - lat)<0.0001:
            my_location = l
            msg.append(('location_match',my_location.name))


    # Make new location
    if my_location is None:
        name = name or 'New'
        my_location = models.Location.objects.create(name=name,
                                                     lon=lon,lat=lat)
        msg.append(('new_location',my_location.name))

    # this delivery
    my_delivery,isnew = models.Delivery.objects.get_or_create(filename=filename,
                                                filename_stored=file_stored,
                                                contributor=contributor,
                                                )

    my_series = models.Series.objects.create(location=my_location,delivery=my_delivery)
    
    try:
        my_history = models.History.objects.filter(location=my_location).latest('version')
    except models.History.DoesNotExist:
        my_history = models.History.objects.create(location=my_location,version=1)

    msg.append(('version',my_history.version))

    # Delete the last day (could have more data now)
    try:
        last = models.Measurement.objects.filter(partof=my_history).latest('timestamp')
        last_date = last.timestamp
        last.delete()
        msg.append(('Timeseries','Append after {}'.format(last_date)))
    except models.Measurement.DoesNotExist:
        last_date = pd.Timestamp(0)
        msg.append(('Timeseries','New'))



    # TODO Check for new version
    dr = data.Hgt_ruw.resample('D',label='center')
    dm = pd.DataFrame(dr.mean())
    dm['maxval'] = dr.max()
    dm['minval'] = dr.min()
    dm['count'] = dr.count()

    nnew =0
    for i,d in dm.ix[last_date:].iterrows():
        print (i,d.Hgt_ruw,d.minval,d.maxval)
        if pd.np.isfinite(d.Hgt_ruw):
            m = models.Measurement.objects.create(partof=my_history,timestamp=i,
                value=d.Hgt_ruw,
                val_min = d.minval,
                val_max = d.maxval)
            nnew+=1

    msg.append(('Last_value','{}'.format(i)))
    msg.append(('New_days',nnew))
    return msg
