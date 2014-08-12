from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import os

from file2pdf.forms import FileForm 
from file2pdf.models import Pdfdata

from django.core.files import File
from pyPdf import PdfFileReader

# Open an existing file using Python's built-in open()
#f = open('/tmp/hello.world')
#myfile = File(f)

def index(request):
    #upload view here
    return render(request, 'file2pdf/index.html')

#def test(request):
    ##return render(request, 'file2pdf/index.html')

#change extension if exists, or add .pdf
def get_pdfname(fname):
    lst = fname.split('.')
    #print 'lst is %s len is %s'%(lst, len(lst))
    if len(lst) > 1:
        lst[-1] = 'pdf'
    else:
        #print 'append!!!!!!!!!'
        lst.append('pdf')
    return '.'.join(lst)


def save2db(pdf_path):
    with open(pdf_path, 'rb') as fin:
        num_pages = PdfFileReader(fin).getNumPages()
        pdfdoc = File(fin)
        #pdfdoc = models.FieldFile.open(pdf_path, 'r')
        f = Pdfdata(filename='dummyname', content=pdfdoc, page_count=num_pages, uploader='dummyuser')
        f.save()
        print '=============save success!!!!!!!!!!!!!'

def handle_upload(f):
    #wrie upload to disk
    fname = str(f)
    pdfname = get_pdfname(fname)
    path = os.path.join(os.path.dirname(__file__), 'temp_upload/'+fname)
    pdf_path = os.path.join(os.path.dirname(__file__), 'temp_upload/'+pdfname)
    print 'path is',path
    print 'pdf path is', pdf_path
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    #convert
    #os.system('unoconv -f pdf -o %s %s'%(out_path, path))
    os.system('unoconv -f pdf %s' % path)

    #save to db
    save2db(pdf_path)

    #clean up files
    os.system('rm %s %s' % (path, pdf_path))


#save to temp, convert, delete temp, return pdf as FileField
#def convert2pdf(userfile):
    ##save to temp
    #print '============gonna convert. userfile type is',type(userfile)
    #write_upload(userfile)
    #return userfile


def success(request):
    return HttpResponse('successful upload!')




def upload(request):
    msg = ''
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            print '==========valid form!!!!!!!!!!!'
            userfile = request.FILES['doc']
            msg = 'upload success! :)'
            try:
                handle_upload(userfile)
            except Exception as e:
                print e
                msg = 'upload failed! :('
    else:
        print '=========GET stuff======='
        form = FileForm()
    l = 'list_content'
    return render(request, 'file2pdf/upload.html', {'form':form, 'list_content_link':l, 'status':msg})
    #return render_to_response('file2pdf/index.html', {'form': form})



def list_content(request):
    # Load documents for the list page
    files = Pdfdata.objects.all()
    #l = reverse('mysite.file2pdf.views.upload')
    l = 'upload'
    return render(request, 'file2pdf/list_content.html', {'files':files, 'upload_link':l})

