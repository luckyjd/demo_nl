from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .forms import DemoLockMeetingForm
import requests, json


ENDPOINT = "edge.polymeeting.com.vn"


def index(request):
    template = loader.get_template("polls/index.html")
    return HttpResponse(template.render({}, request))


def lock_meeting_view(request):
    is_lock = None
    if request.method == 'POST':
        form = DemoLockMeetingForm(request.POST)
        if form.is_valid():

            data = form.data
            device_token_obj = gen_token_device()
            meeting_token_obj = gen_token_meeting(data["meeting_name"], device_token_obj["token"], data["meeting_host_code"])
            get_lock_status = get_meeting_lock_status(data["meeting_name"], meeting_token_obj["token"])
            lock_meeting_flg = lock_unlock_meeting(data["meeting_name"], meeting_token_obj["token"], get_lock_status)
            is_lock = not get_lock_status

    else:
        form = DemoLockMeetingForm()
    return render(request=request, template_name="polls/index.html",
                  context={"form": form, "is_lock": is_lock}
                  )


def gen_token_device():
    url = f"https://{ENDPOINT}/api/client/v2/registrations/Test/request_token"
    headers = {
        'x-pexip-authorization': 'x-pexip-basic VGVzdDpQZXhpcEAxMjM=',
    }
    response = requests.post(url, headers=headers)
    data = json.loads(response.content)
    return data["result"]


def gen_token_meeting(meeting_name, device_token, meeting_code):
    url = f"https://{ENDPOINT}/api/client/v2/conferences/{meeting_name}/request_token"
    payload = {
          "display_name": "demo_web",
          "chosen_idp": "none",
          "sso_token": "none",
          "client_id": "PexRTC",
          "registration_token": device_token,
          "node": ENDPOINT
        }
    headers = {
        'pin': meeting_code,
    }
    response = requests.post(url, data=payload, headers=headers)
    data = json.loads(response.content)
    return data["result"]


def get_meeting_lock_status(meeting_name, meeting_token):
    url = f"https://{ENDPOINT}/api/client/v2/conferences/{meeting_name}/conference_status"
    headers = {
        'token': meeting_token,
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    return data["result"]["locked"]

def lock_unlock_meeting(meeting_name, meeting_token, lock_flg=False):
    url = f"https://{ENDPOINT}/api/client/v2/conferences/{meeting_name}/{'unlock' if lock_flg else 'lock'}"
    headers = {
        'token': meeting_token,
    }
    response = requests.post(url, headers=headers)
    return response.content

