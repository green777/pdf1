from django.db import models

class Pdfdata(models.Model):
    filename = models.CharField(max_length=100)
    content = models.FileField(upload_to='pdf_files')
    page_count = models.IntegerField('total number of pages')
    uploader = models.CharField(max_length=50)
    create_date = models.DateTimeField('date of creation', auto_now_add=True)

    def __unicode__(self):
        return self.filename

