from ..models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def my(request):
    user = request.user.username
    get = Property.objects.all().filter(owner = user)
    if len(get) != 0:
        check = False
    else:
        check = True
    return render(request, "my.html", {
        "check": check,
        "list": get
    })