from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import *
from django.core.mail import send_mail

@login_required(login_url="/login")
def property(request):
    if request.user.manage != "True":
        return redirect("/home")
    else:
        if request.method == "GET":
            return render(request, "new_property.html")
        else:
            if request.POST['owned'] == "True":
                if request.POST['cnic'] and request.POST['reg'] and request.POST['app'] and request.POST['discount'] and request.POST['f']:
                    Property.objects.create(
                        ownerCnic = request.POST['cnic'],
                        owner = request.POST['nam'],
                        reg = request.POST['reg'],
                        app = request.POST['app'],
                        name = request.POST['pro'],
                        type = request.POST['type'],
                        floor = request.POST['floor'],
                        size = request.POST['size'],
                        price = request.POST['price'],
                        discount = request.POST['discount'],
                        fprice = request.POST['f'],
                        location = request.POST['location'],
                        unit = request.POST['unit']
                    )
                    return redirect("/home")
                else:
                    return render(request, "new_property.html", {
                        "error": "Please fill out all fields"
                    })
            else:
                Inv.objects.create(
                    name = request.POST['pro'],
                    type = request.POST['type'],
                    floor = request.POST['floor'],
                    size = request.POST['size'],
                    price = request.POST['price'],
                    unit = request.POST['unit'],
                    location = request.POST['location']
                )
                return redirect("/home")
        
@login_required(login_url="/login")
def newPaymentPlan(request, id):
    if request.user.manage == "True":
        if request.method == "GET":
            if len(Property.objects.all().filter(pk = id)) != 1:
                return redirect("/home")
            else:
                return render(request, "newpay.html", {
                    "id": id
            })
        else:
            PaymentPlan.objects.create(
                property = id,
                type = request.POST['type'],
                date = request.POST['date'],
                amount = "{:,}".format(int(request.POST['amount'])),
                is_paid = request.POST['paid']
            )
            return redirect(F"/view/{id}")

@login_required(login_url="/login")
def rePaymentPlan(request, id):
    if request.user.manage != "True":
        return redirect("/home")
    else:
        if request.method == "GET":
            if len(Property.objects.all().filter(pk = id)) != 1:
                return redirect("/home")
            return render(request, "remove.html", {
                "quaters": PaymentPlan.objects.all().filter(property = id)
            })
            
        
@login_required(login_url="/login")
def rePlan(request):
    if request.method == "POST":
        col = PaymentPlan.objects.get(pk = request.POST['row'])
        i = col.property
        col.delete()
        return redirect("/view/" + str(i))
    else:
        return redirect("/home") 

@login_required(login_url="/login")
def rePro(request, id):
    if request.user.manage == "True":
        if request.method == "GET":
            if len(Property.objects.all().filter(pk = id)) != 1:
                return redirect("/home")
            return render(request, "remove_.html", {
                "id": id
            })
        else:
            pro = Property.objects.get(pk = id)
            pro.delete()
            return redirect("/home")
    else:
        return render("/home")  

@login_required(login_url="/login")
def msg(request):
    if request.method == "GET":
        return render(request, 'msg.html')
    else:
        text = request.POST['text']
        body = f"User-Email: {request.user.email}, User-Msg: {text}"
        send_mail(
            f"{request.user.first_name} {request.user.last_name} has sent you a message",
            body,
            "aventusapp@gmail.com",
            ['aventuspk@gmail.com']
        )
        return redirect("/home")
    
@login_required(login_url="/login")
def details(request):
    if request.user.manage == "True":
        if request.method == "GET":
            return render(request, "new_details.html")
        else:
            if len(UserDetails.objects.all().filter(cnic = request.POST['cnic'])) == 1:
                return render(request, "new_details.html", {
                    "error": "Cnic already exists"
                })
            nominee = Nominee.objects.create(
                name = request.POST['nom'],
                address = request.POST['noma'],
                cnic = request.POST['cnic'],
                relation = request.POST['rel']
            )
            UserDetails.objects.create(
                cnic = request.POST['cnic'],
                fullName = request.POST['fullName'],
                name = request.POST['name'],
                email = '1',
                address = request.POST['add'],
                phone = request.POST['number'],
                occ = request.POST['occ'],
                nat = request.POST['nat'],
                nominee = nominee
            )
            return redirect("/home")
    return redirect("/home")

@login_required(login_url="/login")
def book(request):
    if request.method == "GET":
        return redirect('/home')
    else:
        return render(request, "cont.html", {
            "id": request.POST['id']
        })
    
@login_required(login_url="/login")
def book_(request):
    if request.method == "GET":
        return redirect('/home')
    else:
        pro = Inv.objects.get(pk = request.POST['id'])
        text = request.POST['text']
        body = f'Project: {pro.name}, Unit: {pro.unit}, User-Email: {request.user.email}, User-Message: {text}'
        send_mail(
            f"{request.user.first_name} {request.user.last_name} wants to book a {pro.type}",
            body,
            "aventusapp@gmail.com",
            ['aventuspk@gmail.com']
        )
        return redirect("/home")

@login_required(login_url="/login")
def project(request):
    if request.user.manage != 'True':
        return redirect("/home")
    else:
        if request.method == "GET":
            return render(request, "nproj.html")
        else:
            Projects.objects.create(
                name =  request.POST['name'],
                location = request.POST['location']
            )
            return redirect("/home")

