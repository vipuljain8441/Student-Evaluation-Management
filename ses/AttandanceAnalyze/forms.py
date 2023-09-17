from django import forms

#form to upload the csvfile 
class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')