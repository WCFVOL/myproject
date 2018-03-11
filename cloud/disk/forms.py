from django import forms

class UploadForm(forms.Form) :
    userid = forms.IntegerField()
    nowid = forms.IntegerField()
    file = forms.FileField()