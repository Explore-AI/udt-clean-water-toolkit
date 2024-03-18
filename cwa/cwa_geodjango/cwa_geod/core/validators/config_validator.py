from django import forms


class ConfigValidator(forms.Form):
    method = forms.CharField(max_length=20, required=True)
    srid = forms.IntegerField(required=True)
    query_step = forms.BooleanField(required=True)
    query_limit = forms.BooleanField(required=False)
    query_offset = forms.BooleanField(required=False)
    parallel = forms.BooleanField(required=False, initial=False)
