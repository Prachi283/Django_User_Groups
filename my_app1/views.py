from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User, Group

# Sign Up
def sign_up(request):
	if request.method=="POST":
		fm=SignUpForm(request.POST)
		if fm.is_valid():
			messages.success(request,'Account Created Successdully !')
			user=fm.save()
			group=Group.objects.get(name='Manager')
			user.groups.add(group)
	else:
		fm=SignUpForm()
	return render(request,'my_app1/signup.html',{'form':fm})

# Login View Function
def user_login(request):
	if not request.user.is_authenticated:
		if request.method=="POST":
			fm=AuthenticationForm(request=request,data=request.POST)
			if fm.is_valid():
				uname=fm.cleaned_data['username']   # username is name field from html
				upass=fm.cleaned_data['password']
				user=authenticate(username=uname,password=upass)
				if user is not None:
					login(request,user)
					messages.success(request,'Logged in Successfully !!')
					return render(request,'my_app1/dashboard.html')
		else:
			fm=AuthenticationForm()
		return render(request,'my_app1/userlogin.html',{'form':fm})
	else:
		return render(request,'my_app1/dashboard.html')

# DashBoard
def user_dashboard(request):
	if request.user.is_authenticated:
		return render(request,'my_app1/dashboard.html',{'name':request.user.username})
	else:
		return render(request,'my_app1/userlogin.html')


# Logout
def user_logout(request):
	logout(request)
	return render(request,'my_app1/userlogin.html')
