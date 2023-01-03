from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from .utils import login, get_user_id_by_email, get_user_data, get_refresh_token


def index(request):
    user = None
    error = False
    if request.method == "POST":
        data = request.POST
        email = data.get("login")
        status, data = login(email, data.get("password"))
        if status == 200:
            request.session["access_token"] = data["access_token"]
            request.session["refresh_token"] = data["refresh_token"]
            user_id = get_user_id_by_email(email)
            request.session["user_id"] = user_id
        else:
            error = True
    if access_token := request.session.get("access_token"):
        user_id = request.session["user_id"]
        status, user = get_user_data(access_token, user_id)
        if status == 200:
            return render(request, "index.html", {"user": user["name"]})
        else:
            _, data = get_refresh_token(request.session.get("refresh_token"))
            request.session["access_token"] = data["access_token"]
            return redirect("/")
    return render(request, "login.html", {"error": error})


def logout(request):
    request.session["access_token"] = None
    request.session["refresh_token"] = None
    request.session["user_id"] = None
    return redirect("/")
