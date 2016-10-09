from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

	# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from api.models import Location,History,Measurement

def all(request):
    return render_to_response(
        'api/index.html',
    )

def locations(request):
    ll = Location.objects.all()

    result = {}

    for l in ll:
        locdata = {'name':l.name,'id':l.id}

        if l.project is not None:
            pname = l.project.name
        else:
            pname = 'Overig'

        if pname in result.keys():
            result[pname]['locations'].append(locdata)
        else:
            result[pname] = {'name':pname,'locations':[locdata]}

    return JsonResponse({'projects':list(result.values())})
    # pl = defaultdict(list)
    # for l in ll:
    #     if l.project is not None:
    #         p = l.project


    #     'Overig'
    #     pl[p].append({'name':l.name,'id':l.id})
    # return JsonResponse(pl)

def timeseries(request):
    id = int(request.GET['id'])
    do_range = request.GET.get('ranges',False)
    print ('Go make SERIES for {}'.format(id))
    h = History.objects.filter(location_id=id).latest('version')
    mm = Measurement.objects.filter(partof=h)

    offset = mm[0].value
    result = [[m.timestamp.isoformat(),round(m.value-offset,4)] for m in mm]

    if do_range:
        print ('Go make RANGES for {}'.format(id))
        ranges = [[m.timestamp.isoformat(),round(m.val_min-offset,4),round(m.val_max-offset,4)] for m in mm]

        return JsonResponse({'data':result, 'ranges':ranges,
                             'location':h.location.name,'version':h.version,'offset':round(offset,4)})

    return JsonResponse({'data':result,'location':h.location.name,'version':h.version,'offset':round(offset,4)})
    