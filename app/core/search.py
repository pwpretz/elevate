from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import *
from .error import error

@login_required(login_url="/login")
def staff(request):
    if request.user.manage == "True":
        if request.method == "GET":
            return redirect("/home")
        else:
            if len(User.objects.all().filter(cnic = request.POST['cnic'])) != 1:
                return render(request, "search.html", {
                    "check": True
                })
            else:
                return render(request, "search.html", {
                    "user": User.objects.get(cnic = request.POST['cnic'])
                })
    else:
        return redirect("/home")

@login_required(login_url="/login")
def sold(request):
    if request.method == "GET":
        return redirect("/home")
    else:
        res = Property.objects.all().filter(owner = request.POST['unit'])
        if len(res) < 1:
            return render(request, "sSold.html", {
                "check": "No properties Found"
            })
        return render(request, "sSold.html", {
            "results": res
        })

def inv(request):
    if request.method == "GET":
        return redirect("/home")
    else:
        p = Inv.objects.all().filter(unit = request.POST['unit'])
        if len(p) < 1:
            return render(request, "invsearch.html", {
                "check": "No Property Found"
            })
        return render(request, "invsearch.html", {
            "properties": p
        })