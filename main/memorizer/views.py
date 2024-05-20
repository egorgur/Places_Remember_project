import json

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from memorizer.models import Memo


def redirect_to_main(request):
    return HttpResponseRedirect("/memorizer/memories")


def memories_menu_view(request):
    if request.method == "GET":
        has_memories = False
        memories = list(Memo.objects.filter(user=request.user).values())
        print(memories)
        if len(memories) > 0:
            has_memories = True
        return render(
            request=request,
            template_name="memorizer/memories.html",
            context={
                "username": request.user.username,
                "has_memories": has_memories,
                "memories": memories
            }
        )


def memo_view(request, pk):
    if request.method == "GET":
        memo = Memo.objects.get(id=pk)
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
    if request.method == "POST":
        try:
            name = request.POST["name"]
            comment = request.POST["comment"]
            position = json.loads(request.POST["position"])
            print(name, comment, position)
            memo = Memo.objects.get(id=pk)
            memo.name = name
            memo.text = comment
            memo.position_x = position['x']
            memo.position_y = position['y']
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
