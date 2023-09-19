from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import *

@login_required(login_url="/login")
def staff(request):
    if request.method == "GET":
        if request.user.manage == "True":
            staff = User.objects.all().filter(manage = "True")
            return render(request, "staff.html", {
                "staff": staff
            })
        else: 
            return redirect("/home")
        
@login_required(login_url="/login")
def mstaff(request, id):
    if request.user.manage == "True":
        if request.method == "GET":
            if len(User.objects.all().filter(pk = id)) == 1:
                return render(request, "mstaff.html", {
                    "user": User.objects.get(pk = id)
                })
            else:
                return render(request, "mstaff.html", {
                    "check": True
                })
        else:
            user = User.objects.get(pk = id)
            if 'True' in request.POST.getlist('staff'):
                user.manage = "True"
                user.save()
            else:
                user.manage = "False"
                print(user.cnic)
                user.save()
            return redirect("/info/" + str(id))
        
@login_required(login_url="/login")
def property(request):
    if request.user.manage != "True":
        return redirect("/home")
    else:
        if request.method == "GET":
            return render(request, "mpro.html", {
                "pro": Property.objects.all()
            })

@login_required(login_url="/login")
def search_pro(request):
    if request.method == "GET":
        return redirect("/")
    elif request.user.manage != "True":
        return redirect("/home")
    else:
        if len(Property.objects.all().filter(unit = request.POST['unit'])) < 1:
            return render(request, "pro_search.html", {
                "check": True
            })
        pro = Property.objects.all().filter(unit = request.POST['unit'])
        return render(request, "pro_search.html", {
            "pros": pro,
        })

@login_required(login_url="/login")
def sold(request):
    return render(request, "sold.html", {
        "props": Property.objects.all()
    })

@login_required(login_url="/login")
def delInv(request, id):
    if request.method == "GET":
        if request.user.manage != "True":
            return redirect("/home")
        return render(request, "dl.html",{
            "id": id
        })
    else:
        p = Inv.objects.all().filter(pk = id)
        if len(p) != 1:
            return redirect("/home")
        p[0].delete()
        return redirect("/home")

@login_required(login_url="/login")
def delp(request, id):
    if request.user.manage != "True":
        return redirect("/home")
    elif request.method == "GET":
        return render(request, "del1.html", {
            "id": id
        })
    else:
        p = Projects.objects.all().filter(pk = id)
        if len(p) != 1:
            return redirect("/home")
        p[0].delete()
        return redirect("/home")
    
@login_required(login_url='/login')
def delete_user(request, id):
    if request.user.manage == "True":
        if request.method == "GET":
            return render(request, "delete_user.html", {
                "id": id
            })
        else:
            user = User.objects.all().filter(pk = id)
            if len(user) != 1:
                return redirect("/home")
            else:
                user[0].delete()
                return redirect("/home")

@login_required(login_url='/login')
def edit_user(request, id):
    if request.user.manage == "True":
        user = User.objects.all().filter(pk = id)
        if request.method == "GET":
            if len(user) != 1:
                return redirect("/home")
            return render(request, "edit_user.html", {
                "id": id,
                "iuser": user[0]
            })
        else:
            user = user[0]
            user.cnic = request.POST['number']
            user.email = request.POST['email']
            user.first_name = request.POST['fullname']
            user.last_name = request.POST['namel']
            user.save()
            return redirect("/")
        
@login_required(login_url='/login')
def edit_details(request, id):
    if request.user.manage == "True":
        d = UserDetails.objects.all().filter(pk = id)
        if len(d) != 1:
            return redirect("/")
        return render(request, "new_details.html", {
            "d": d[0]
        })