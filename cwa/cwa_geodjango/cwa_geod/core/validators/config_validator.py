from django import forms


class ConfigValidator(forms.Form):
    method = forms.CharField(max_length=20, required=True)
    srid = forms.IntegerField(required=True)
    parallel = forms.BooleanField(required=False)
