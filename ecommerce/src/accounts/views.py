from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm,GuestForm
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.utils.http import is_safe_url

from .models import GuestEmail


def guest_register_view(request):
    guest_form = GuestForm(request.POST or None)
    context = {"form":guest_form}
    
    # where to go after user login or register
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    
    print(next_get)
    print(next_post)
    print(redirect_path)
    print(request.META.items())
    
    if guest_form.is_valid():
        current_email = guest_form.cleaned_data['email']
        print("guest email:" + current_email)
        #store the guest email in database
        new_guest_email = GuestEmail.objects.create(email=current_email)
        # put the id into session variable, to check if the email already exists and if it has a billing profile
        request.session['guest_email_id'] = new_guest_email.id
        print(new_guest_email.id)
        print(new_guest_email.email)
        print(redirect_path)
    
        if is_safe_url(redirect_path,request.get_host()):
            print("redirect path:" + redirect_path)
            return redirect(redirect_path)
        else:
            return redirect("/cart/checkout/")
        
    return redirect("/cart/checkout/")



def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {"form":login_form}
    
    # where to go after user login or register
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    
    print(next_get)
    print(next_post)
    print(redirect_path)
    
    if login_form.is_valid():
        print(login_form.cleaned_data)
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            try:
                del request.session['guest_email_id']
            except:
                pass
            
            if is_safe_url(redirect_path,request.get_host()):
                print(redirect_path)
                return redirect(redirect_path)
            else:
                return redirect("/products")
        else:
            # Return an 'invalid login' error message.
           context['error']="Wrong username or password"
        
    return render(request,'login.html',context)

def logout_view(request):
    logout(request)
    return redirect("products")

User = get_user_model()
def register_page(request):
    register_form = RegisterForm(request.POST or None)
    message = "You are Registered!"
    context = {"form":register_form,"message":message}
    if register_form.is_valid():
        print(register_form.cleaned_data)
        username = register_form.cleaned_data.get('username')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        new_user = User.objects.create_user(username,email,password)
        return redirect("/login")
    
    return render(request,'register.html',context)