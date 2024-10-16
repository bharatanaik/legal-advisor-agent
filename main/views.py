from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "main/index.html")

@login_required
def dashboard(request):
    return render(request, "main/dashboard.html")

def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard'))
    return render(request, "registration/signup.html", {
        "form":form
    })
 
