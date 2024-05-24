import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from memorizer.models import Memo
from vk_auth.views import get_user_vk_data, update_user_vk_data
from vk_auth.models import UserVkData


def redirect_to_main(request):
    return HttpResponseRedirect("/memorizer/memories")


def memories_menu_view(request):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseRedirect("/auth/")
    print(request)
    if request.method == "GET":
        vk_sdk_version = 5.199
        user_vk_data = UserVkData.objects.get(user=request.user)
        access_token = user_vk_data.access_token
        vk_id = user_vk_data.vk_id
        response = get_user_vk_data(vk_sdk_version, access_token, vk_id)
        if "error_code" not in response:
            first_name = response["first_name"]
            last_name = response["last_name"]
            photo_50 = response["photo_50"]
            print(vk_id, first_name, last_name, photo_50)
            update_user_vk_data(vk_id, first_name, last_name, access_token)
        else:
            return HttpResponseRedirect("/auth/")
        has_memories = False
        memories = list(Memo.objects.filter(user=request.user).values())
        print(memories)
        if len(memories) > 0:
            has_memories = True
        return render(
            request=request,
            template_name="memorizer/memories.html",
            context={
                "first_name": first_name,
                "last_name": last_name,
                "photo_href": photo_50,
                "has_memories": has_memories,
                "memories": memories
            }
        )


def memo_view(request, pk):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseRedirect("/auth/")
    print(request)
    if request.method == "GET":
        if Memo.objects.filter(id=pk).exists():
            memo = Memo.objects.get(id=pk)
            if memo.user != request.user:
                return HttpResponseRedirect("/memorizer/memories")
            return render(
                request=request,
                template_name="memorizer/view_memo.html",
                context={
                    "name": memo.name,
                    "comment": memo.text,
                    "position_x": memo.position_x,
                    "position_y": memo.position_y,
                }
            )
        else:
            return HttpResponseRedirect("/memorizer/memories")
    if request.method == "POST":
        try:
            name = request.POST["name"]
            comment = request.POST["comment"]
            position = json.loads(request.POST["position"])
            print(name, comment, position)
            memo = Memo.objects.get(id=pk)
            memo.name = name
            memo.text = comment
            memo.position_x = position["x"]
            memo.position_y = position["y"]
            memo.save()
            response = {
                "success": True
            }
        except Exception as e:
            print(e)
            response = {
                "success": False,
                "error": repr(e)
            }
        return JsonResponse(response)


def create_memo_view(request):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseRedirect("/auth/")
    print(request)
    if request.method == "GET":
        return render(
            request=request,
            template_name="memorizer/create_memo.html"
        )
    if request.method == "POST":
        try:
            name = request.POST["name"]
            comment = request.POST["comment"]
            position = json.loads(request.POST["position"])
            print(name, comment, position)
            memo = Memo.objects.create(
                user=request.user,
                name=name,
                text=comment,
                position_x=position['x'],
                position_y=position['y']
            )
            memo.save()
            response = {
                "success": True
            }
        except Exception as e:
            print(e)
            response = {
                "success": False,
                "error": repr(e)
            }
        return JsonResponse(response)


def delete_memo(request, pk):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseRedirect("/auth/")
    print(request)
    if request.method == "GET":
        if Memo.objects.filter(id=pk).exists() and (Memo.objects.get(id=pk).user == request.user):
            memo = Memo.objects.get(id=pk)
            memo.delete()
        return HttpResponseRedirect("/memorizer/memories")
