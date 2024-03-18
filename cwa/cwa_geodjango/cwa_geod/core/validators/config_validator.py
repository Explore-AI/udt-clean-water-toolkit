from django import forms


class ConfigValidator(forms.Form):
    method = forms.CharField(max_length=20, required=True)
    srid = forms.IntegerField(required=True)
    query_step = forms.IntegerField(required=True)
    query_limit = forms.IntegerField(required=False, initial=1000)
    query_offset = forms.IntegerField(required=False, initial=0)
    parallel = forms.BooleanField(required=False, initial=False)
