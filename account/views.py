from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
from plantAI.models import PlantInfo

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            transfer_temp_plants_to_user(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})

def transfer_temp_plants_to_user(request, user):
    temp_plants = request.session.get("temporary_plants", [])
    for plant_data in temp_plants:
        PlantInfo.objects.create(
            user=user,
            image=plant_data["image_path"],
            prediction=plant_data["prediction"]
        )
    request.session.pop('temporary_plants', None)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, 'account/logout.html')