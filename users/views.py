from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm
# Create your views here.

def login(request):
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')
        checkin = request.POST.get('checkin')
        
        user = authenticate(request, username = name, password = password)
        
        if user is not None:
            auth_login(request, user)
            
            if checkin:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days (Remember Me)
            else:
                request.session.set_expiry(0)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')        

    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("signup")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("login")  # Redirect to login page

    return render(request, "signup.html")