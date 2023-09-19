from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")
def contact(request):
    return render(request, "contact.html")

@login_required(login_url="/login")
def property(request, id):
    if len(Property.objects.all().filter(pk = id)) == 1:
        if len(PaymentPlan.objects.all().filter(property = Property.objects.get(pk = id).id)) >= 1:
            plan = PaymentPlan.objects.all().filter(property = id);
            return render(request, "view.html", {
                "view": Property.objects.get(pk = id),
                "user": request.user,
                "payments": plan,
            })
        else:
            return render(request, "view.html", {
                "view": Property.objects.get(pk = id),
                "check": True
            })
        
def inv(request, name):
    pr = Projects.objects.all().filter(pk = name)
    return render(request, "inv.html", {
        "properties": Inv.objects.all().filter(name = pr[0].name),
        "name": pr[0].name
    })

def invsee(request, id):
    if len(Inv.objects.all().filter(pk = id)) != 1:
        return render("/")
    return render(request, "invsee.html", {
        "pro": Inv.objects.get(pk = id)
    })

@login_required(login_url="/login")
def info(request, id):
    if len(User.objects.all().filter(pk = id)) != 1:
        return redirect('/')
    if len(UserDetails.objects.all().filter(cnic = User.objects.get(pk = id).cnic)) == 1:
        return render(request, "info.html", {
            "info": UserDetails.objects.get(cnic = User.objects.get(pk = id).cnic),
            "iuser": User.objects.get(pk = id)
        })
    else:
        return render(request, "info.html", {
            "check": True,
            "iuser": User.objects.get(pk = id)
        })

@login_required(login_url="/login")
def delete(request, id):
    if request.user.manage == "True":
        if request.method == "GET":
            if len(UserDetails.objects.all().filter(pk = id)) != 1:
                return redirect("/")
            return render(request, "delete_.html", {
                "id": id
            })
        else:
            obj = UserDetails.objects.get(pk = id)
            obj.delete()
            return redirect("/")

@login_required(login_url="/login")
def manage(request):
    if request.user.manage == "True": 
        if request.method == "POST":
            obj = User.objects.all().filter(cnic = request.POST['unit'])
            if len(obj) < 1:
                return render(request, "smanage.html", {
                    "check": True
                })
            return render(request, "smanage.html", {
                "obj": User.objects.get(cnic = request.POST['unit'])
            })

        else:
            return render(request, "manage_users.html", {
                "users": User.objects.all()
            })
        
@login_required(login_url="/login")
def bank(request):
    return render(request, 'bank.html')

def projects(request):
    return render(request, "proj.html", {
        "projects": Projects.objects.all()
    })

def hidebar(request):
    return render(request, "assetlinks.json", content_type="application/json")

def popup(request):
    if request.method == "GET":
        popup = Popup.objects.all()
        if len(popup) != 1:
            return redirect("/home")
        return render(request, "popup.html", {
            "url": popup[0]
        })
    else:
        popup = Popup.objects.all()
        if len(popup) == 1:
            popup[0].delete()
        if request.POST['type'] == "True":
            url = request.POST['url'].split('/')
            url = url[3].replace("watch?v=", " ").strip()
            Popup.objects.create(
                type = "video",
                url = url
            )
            return redirect("/")
        else:
            Popup.objects.create(
                type = "img",
                url = request.POST['url']
            )
            return redirect("/")

def new_popup(request):
    if request.method == "GET":
        return render(request, "new_ad.html")
    else:
        pop = Popup.objects.all()
        if len(pop) == 1:
            pop[0].delete()
            return redirect("/")
        else:
            return redirect("/")