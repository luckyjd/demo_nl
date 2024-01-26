from django import forms


class DemoLockMeetingForm(forms.Form):
    registration_host = forms.CharField(required=True, label="Registration Host")
    alias = forms.CharField(required=True, label="Alias")
    username = forms.CharField(required=True, label="Username")
    password = forms.CharField(required=True, label="Password")
    meeting_name = forms.CharField(required=True, label="Meeting Name")
    meeting_host_code = forms.IntegerField(required=True, label="Meeting Code")