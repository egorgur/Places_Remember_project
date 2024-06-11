import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.settings import VK_APP_SERVER_KEY, VK_APP_ID
from django.contrib.auth.models import User
from .models import UserVkData
from django.contrib.auth import login, logout

import requests


# Create your views here.
def auth_view(request):
    print("auth view")
    return render(
        request=request,
        template_name="vk_auth/authorization.html",
        context={
            "VK_APP_ID": VK_APP_ID
        },
    )


def auth_processor(request):
    print(request)
    if request.method == "GET":
        vk_sdk_version = 5.199
        payload = json.loads(request.GET.get("payload"))
        if payload["type"] == "silent_token":
            silent_token = payload["token"]
            uuid = payload["uuid"]
            response = exchange_silent_on_access_token(vk_sdk_version, silent_token, uuid, VK_APP_SERVER_KEY)
            print(response)
            if "error_code" not in response:
                access_token = response["access_token"]
                vk_user_id = response["user_id"]
                response = get_user_vk_data(api_version=vk_sdk_version, access_token=access_token,
                                            user_id=vk_user_id)
                if "error_code" not in response:
                    first_name = response["first_name"]
                    last_name = response["last_name"]
                    photo_50 = response["photo_50"]
                    print(vk_user_id, first_name, last_name, photo_50)
                    if UserVkData.objects.filter(vk_id=vk_user_id).exists():
                        user = update_user_vk_data(vk_user_id, first_name, last_name, access_token)
                    else:
                        user = create_user_with_vk_data(vk_user_id, first_name, last_name, access_token)
                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect("/memorizer/")
                else:
                    print("error in", response)
                    return HttpResponseRedirect("/auth/")
            print("error in", response)
            return HttpResponseRedirect("/auth/")
        print("error in", payload)
        return HttpResponseRedirect("/auth/")
    else:
        return HttpResponse("only GET is allowed")


def leave_account(request):
    logout(request)
    HttpResponseRedirect("/auth/")


def exchange_silent_on_access_token(api_version, silent_token, uuid, server_token):
    params = {
        "v": api_version,
        "token": silent_token,
        "access_token": server_token,
        "uuid": uuid
    }
    response = requests.get("https://api.vk.com/method/auth.exchangeSilentAuthToken/", params=params).json()
    print(response)
    if "error" in response:
        return response["error"]
    if "response" in response:
        return response["response"]


def get_user_vk_data(api_version, access_token, user_id):
    params = {
        "v": api_version,
        "access_token": access_token,
        "user_ids": user_id,
        "fields": "first_name,last_name,photo_50"
    }
    response = requests.get("https://api.vk.com/method/users.get/", params=params).json()
    print(response)
    if "error" in response:
        return response["error"]
    if "response" in response:
        return response["response"][0]


def update_user_vk_data(vk_id, first_name, last_name, access_token):
    try:
        user_vk_data = UserVkData.objects.get(vk_id=vk_id)
        user = user_vk_data.user
        user.first_name = first_name
        user.last_name = last_name
        user_vk_data.access_token = access_token
        user.save()
        user_vk_data.save()
        print("updated ", first_name, " data")
        return user
    except Exception as e:
        print("failed to update user_vk_data ", repr(e))
        return None


def create_user_with_vk_data(vk_id, first_name, last_name, access_token):
    try:
        user = User.objects.create(
            username=str(vk_id),
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        user_vk_data = UserVkData.objects.create(
            user=user,
            vk_id=vk_id,
            access_token=access_token
        )
        user_vk_data.save()

        print("created user ", first_name)
        return user
    except Exception as e:
        print("failed to create user ", repr(e))
        return None
