from django.shortcuts import render, redirect
from django.core.mail import send_mail
from ..models import *
from .error import error
from django.contrib.auth import authenticate, logout
import random
from django.contrib.auth import login as ll
from django.contrib.auth.decorators import login_required

def elogin(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        cnic = request.POST['cnic']
        password = request.POST['pass']

        user = authenticate(username = str(cnic), password = password)
        if user is not None:
            d1 = random.randint(1, 9)
            d2 = random.randint(1, 9)
            d3 = random.randint(1, 9)
            d4 = random.randint(1, 9)
            code = str(d1) + str(d2) + str(d4) + str(d3)
            content = str(code) + " Here is your aventus login code !"
            send_mail(
                str(code) + " Aventus app login code",
                content,
                "aventusapp@gmail.com",
                [user.email],
            )
            c = Code.objects.create(
                code = code,
                cnic = request.POST['cnic'],
                password = request.POST['pass']
            )
            return redirect("/verify/" + str(c.id))
        else:
            return render(request, "login.html", {
                "error": "Incorrect login details"
            })
@login_required(login_url='/login')
def register(request):
    if request.user.manage != "True":
        return redirect("/home")
    elif request.method == "GET":
        return render(request, "register.html")
    else:
        if len(User.objects.all().filter(cnic = request.POST['number'])) == 1:
            return render(request, "register.html", {
                "error": "CNIC number already in-use"
            })
        if len(User.objects.all().filter(email = request.POST['email'])) == 1:
            return render(request, "register.html", {
                "error": "Email adress already in-use"
            })
        if len(request.POST['password']) < 8:
            return render(request, "register.html", {
                "error": "Password must be atleast 8 charecters long"
            })
        if len(request.POST['number']) != 13:
            return render(request, "register.html", {
                "error": "Invalid CNIC"
            })
        user = User.objects.create_user(
            email = request.POST['email'],
            password = request.POST['password'],
            cnic = request.POST['number'],
            username = request.POST['number'],
            last_name = request.POST['namel'],
            first_name = request.POST['fullname']
                    )
        user.save()
        return redirect("/home")
        
def verify(request, idd):
        if len(Code.objects.all().filter(pk = idd)) == 1:
            if request.method == "GET":
                return render(request, "verify.html", {
                    "id": idd
                })
            else:
                vercode = Code.objects.get(pk = idd)
                code = request.POST['code']

                if len(code) != 4:
                    return render(request, "verify.html", {
                    "id": idd,
                    "error": "Invalid Code"
                })

                if vercode.code == code:
                    user = authenticate(username = str(vercode.cnic), password = vercode.password)
                    ll(request, user)
                    vercode.delete()
                    return redirect("/home")
                else:
                    return render(request, "verify.html", {
                    "id": idd,
                    "error": "Invalid Code"
                })
        else:
            return error(request, "404", "Page not found")

def elogout(request):
    logout(request)
    return redirect("/home")

@login_required(login_url="/login")
def changePass(request):
    if request.method == "GET":
        return render(request, "change.html")
    else:
        curr = request.POST['curr']
        new = request.POST['pass']

        if len(new) < 8:
            return render(request, "change.html", {
                "error": "New password must be 8 or longer"
            })
        print(request.user.check_password(curr))
        check = request.user.check_password(curr)
        if not check:
            return render(request, "change.html", {
                "error": "Password is incorrect"
            })
        else:
            d1 = random.randint(1, 9)
            d2 = random.randint(1, 9)
            d3 = random.randint(1, 9)
            d4 = random.randint(1, 9)
            code = str(d1) + str(d2) + str(d4) + str(d3)
            content = str(code) + " Here is your aventus password change code !"
            send_mail(
                str(code) + " Aventus app password change code",
                content,
                "aventusapp@gmail.com",
                [request.user.email],
            )
            c = change.objects.create(
                code = code,
                new = new
            )
            return redirect("/pass/verify/" + str(c.id))

@login_required(login_url='/login')
def changePassVer(request, id):
    if len(change.objects.all().filter(pk = id)) < 1:
        return redirect("/home")
    elif request.method == "GET":
        return render(request, "verify1.html", {
                    "id": id
                })
    else:
        c = change.objects.get(pk = id)
        code = request.POST['code']

        if len(code) < 4 or code != c.code:
            return render(request, "verify1.html", {
                "error": "invalid code"
            })
        u = User.objects.get(cnic = request.user.cnic)
        u.set_password(c.new)
        u.save()
        c.delete()
        ll(request, u)
        return redirect("/home")
    
def forgot(request):
    if request.method == "GET":
        return render(request, "forgot.html")
    else:
        cnic = request.POST['cnic']
        user = User.objects.all().filter(username = cnic)
        if len(user) != 1:
            return render(request, "forgot.html", {
                "error": "Invalid Cnic"
            })
        
        return redirect('/forgot/2/' + str(cnic))

def forgot1(request, cnic):
    if request.method == "GET":
        if len(User.objects.all().filter(username = cnic)) != 1:
            return redirect("/")
        return render(request, "forgot_2.html", {
            "cnic": cnic
        })
    else: 
        user = User.objects.get(username = cnic)
        pas = request.POST['password']
        if len(pas) < 8:
            return render(request, "forgot2.html", {
                "error": "Password must be 8 or longer",
                "cnic": cnic
            })
        d1 = random.randint(1, 9)
        d2 = random.randint(1, 9)
        d3 = random.randint(1, 9)
        d4 = random.randint(1, 9)
        code = str(d1) + str(d2) + str(d3) + str(d4)
        c = change.objects.create(
            code = code,
            new = pas
        )
        send_mail(
                str(code) + " Aventus app password change code",
                str(code) + " Password reset code for aventus app",
                "aventusapp@gmail.com",
                [user.email],
            )
        return redirect("/forgot/3/" + str(c.id) + "/" + cnic)
    
def forgot2(request, id, cnic):
    if request.method == "GET":
        return render(request, "ver.html", {
            id: id
        })
    else:
        code = change.objects.all().filter(pk = id)
        input1 = request.POST['code']
        if len(code) != 1:
            return redirect("/")
        elif len(input1) < 4:
            return render(request, "ver.html", {
                "id": id,
                "error": "Code must be 4 digits"
            })
        elif code[0].code != input1:
            return render(request, "ver.html", {
                "id": id,
                "error": "Invalid code"
            })
        user = User.objects.all().filter(username = cnic)
        if len(user) != 1:
            return redirect("/")
        user = user[0]
        user.set_password(code[0].new)
        user.save()
        return redirect("/login")