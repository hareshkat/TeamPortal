from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import TeamMember
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
  if request.user.id != None:
    return redirect("/")
  else:
    msg = ''
    if request.method == 'POST':
      username = request.POST['username']
      password =  request.POST['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect("/home")
      else:
          msg = 'Invalid credentials'
    return render(request, "registration/login.html", {'msg':msg})


# @login_required(login_url="/login/")
def profile(request):

  if request.method == 'POST':
    aboutme = request.POST['about_me']
    user_profile = TeamMember.objects.get(pk=request.user.id)
    user_profile.about_me = aboutme
    user_profile.save()

  user_data = TeamMember.objects.filter(name_id = request.user.id).values()
  for u in user_data:
    data = {
    'emp_id' : u['emp_id'],
    'contact_no' : u['contact_no'],
    'dob' : u['dob'],
    'gender' : u['gender'],
    'status' : u['status'],
    'aboutme' : u['about_me']
    }
    break
  return render(request, "registration/user_profile.html", data)


# def handler404(request, exception, template_name="error/error-404.html"):
#   response = render(request, "error/error-404.html")
#   response.status_code = 404
#   return response

def handler403(request, exception=None):
  return render(request, "error/error-403.html", status=403)


def handler404(request, exception=None):
  return render(request, "error/error-404.html", status=404)

def handler500(request, exception=None):
  return render(request, "error/error-500.html", status=500)
