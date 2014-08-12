from django import forms

class FileForm(forms.Form):
    doc = forms.FileField(label='choose a file to upload, haha')

