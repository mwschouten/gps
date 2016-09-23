                     # import_file.py
import pandas as pd
import re
from api import models

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



def import_xlsx(file,name=None,file_stored=None,contributor=None):
    """ For now, assume that it is an Antea GPS file with proper columns
    """
    # file = 'data/AGBA4.xlsx'
    # name = None
    # contributor=None
    # file_stored=None

    print ('\n\n FILE ',file)
    print ('\n\n NAME ',name)
    print ('\n\n')


    data = pd.read_excel(file)
    data = data.set_index('Date_time')

    msg = [('filename',file),('loc_name_provided',name)]

    if not 'Hgt_ruw' in data.columns.values:
        msg.append(('ERROR','No Hgt_ruw columns in data'))
        return msg


    lon = get_decimal_degree(data.Long[0])
    lat = get_decimal_degree(data.Lat[0])

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
    my_delivery,isnew = models.Delivery.objects.get_or_create(filename=file,
                                                filename_stored=file_stored,
                                                contributor=contributor)
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
