from django import forms


class DemoLockMeetingForm(forms.Form):
    registration_host = forms.CharField(required=True, label="Máy chủ")
    alias = forms.CharField(required=True, label="Tên Định Danh")
    username = forms.CharField(required=True, label="Tên Tài Khoản")
    password = forms.CharField(required=True, label="Mật Khẩu")
    meeting_name = forms.CharField(required=True, label="Tên Hội Nghị")
    meeting_host_code = forms.IntegerField(required=True, label="Mã Hội Nghị")