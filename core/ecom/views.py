from uuid import uuid4
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import UserConfirm
from .utils import send_code


def user_registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')

        # Check if user with this email already exists
        if User.objects.filter(username=email).exists():
            return render(request, 'registration_error.html', {'error_message': 'User with this email already exists.'})

        # Generate code and token
        code = send_code(email=email)
        token = uuid4()

        try:
            # Create user in Django's User model for authentication
            django_user = User.objects.create_user(username=email, email=email, password=password)

            # Save additional details in your UserConfirm model
            user = UserConfirm(
                email=email,
                name=name,
                surname=surname,
                phone=phone,
                address=address,
                city=city,
                country=country,
                postal_code=postal_code,
                code=code,
                token=token
                # add other fields as needed
            )
            user.save()

            # Optionally, authenticate and login the user
            authenticated_user = authenticate(username=email, password=password)
            if authenticated_user:
                login(request, authenticated_user)

            # Render code confirmation page with token
            response = render(request, 'code.html', {"token": token})
            response.set_cookie('token', token)
            return response
        
        except IntegrityError:
            return render(request, 'registration_error.html', {'error_message': 'Error creating user.'})

    return render(request, 'index.html')





def code_confirm(request):
    if request.method == "POST":
        # Code confirmation handling
        code = request.POST.get('code').strip()
        token = request.COOKIES.get('token')
        
        try:
            # Verify code and token in UserConfirm model
            user = UserConfirm.objects.get(token=token, code=code, is_active=False)
            user.is_active = True
            user.save()
            return render(request, 'code.html', {"token": token, "message": "Success"})
        except UserConfirm.DoesNotExist:
            return render(request, 'code.html', {"token": token, "message": "Error"})
    
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your actual home page name
        
        # If authentication fails, you can handle it here (e.g., show error message)
        return render(request, 'login.html', {'error_message': 'Invalid credentials. Please try again.'})
    
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')  # Replace with your home page template
