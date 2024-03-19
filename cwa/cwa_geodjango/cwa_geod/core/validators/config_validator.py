from django import forms
from django.core.exceptions import ValidationError


class ConfigValidator(forms.Form):
    method = forms.CharField(max_length=20, required=True)
    srid = forms.IntegerField(required=True)
    query_step = forms.IntegerField(required=True)
    query_limit = forms.IntegerField(required=False)
    query_offset = forms.IntegerField(required=False)
    parallel = forms.BooleanField(required=False)
    thread_count = forms.IntegerField(required=False)
    processor_count = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        parallel = cleaned_data.get("parallel")
        thread_count = cleaned_data.get("thread_count")
        processor_count = cleaned_data.get("thread_count")

        if parallel and not (thread_count or processor_count):
            raise ValidationError(
                "If parallel is set to 'True' both 'thread_count' and 'processor_count' must be specified."
            )
