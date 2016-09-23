from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

	# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# from files.models import Document
# from files.forms import DocumentForm

def all(request):
    return render_to_response(
        'api/index.html',
    )

