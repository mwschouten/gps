# from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from files.models import Document
from files.forms import DocumentForm
from django.contrib.auth.decorators import login_required
from experts.import_file import import_xlsx

# @login_required
# def list(request):
#     # Handle file upload
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Document(docfile = request.FILES['docfile'])
#             newdoc.save()

#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('files.views.list'))
#     else:
#         form = DocumentForm() # A empty, unbound form

#     # Load documents for the list page
#     documents = Document.objects.all()

#     # Render list page with the documents and the form
#     return render_to_response(
#         'files/list.html',
#         {'documents': documents, 'form': form},
#         context_instance=RequestContext(request)
#     )

@login_required
def submit(request):

    print('REQUEST.FILES', request.FILES)
    print('REQUEST.FILES', request.FILES['docfile'].__dict__)
    print('REQUEST.POST', request.POST)
    name = request.FILES['docfile']._name
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        print('FORM ', form)
        print('FORM IS VALID', form.is_valid())

        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            print ('NEWDOC ',newdoc)
            print ('NEWDOC ',newdoc.__dict__)
            print ('NEWDOC ',newdoc.docfile.__dict__)
            file_stored = 'media/' + newdoc.docfile.name
            print ('FILE STORED ',file_stored)

            ok,matched = import_xlsx(filename = request.FILES['docfile']._name,
                                     file_stored = file_stored)


            # Respond ANYWAY
            return JsonResponse({
                'ok':True,
                'id':newdoc.id,
                'name':request.FILES['docfile']._name,
                'size':request.FILES['docfile']._size,
                'match':'new'}
                )
        else:
            return JsonResponse({
                'ok':False,
                'errors':form.errors}
                )
            