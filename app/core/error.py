from django.shortcuts import render, redirect

def error(request, error, code):
    return render(request, "error.html", {
        "error": error,
        "code": code
    })