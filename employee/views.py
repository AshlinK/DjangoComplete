from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse,get_object_or_404,HttpResponse
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from demo.decorators import role_required


def user_login(request):
    context=dict()
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user=user)
            if request.GET.get('next',None):
               return HttpResponseRedirect(request.GET['next'])

            request.session['user_id']=user.id
            request.session.create()
            return HttpResponseRedirect(reverse("success"))
        else:
            context['error']="Provide valid credentials !!"
            return render(request,'auth/login.html',context)

    else:
        return render(request,'auth/login.html',context)
        
def success(request):
    if request.session.get('user_id'):
        return render(request,'auth/success.html')
    return HttpResponseRedirect(reverse("user_login"))

@login_required(login_url="/login/")
def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponse("You are logged out!!")

@login_required(login_url="/login/")
def employee_list(request):
    if request.session.get('user_id'):
        print(request.user.groups.all())
        context={}
        context['users']=User.objects.all()
        context['title']='Employees'
        context['blurb']="<p>You are <em>pretty</em> smart!</p>"
        return render(request,'employee/index.html',context)
    return HttpResponseRedirect(reverse("user_login"))

    

def employee_details(request,id):
    if request.session.get('user_id'):
        context={}
        context['user']=get_object_or_404(User,id=id)
        return render(request,'employee/details.html',context) 
    return HttpResponseRedirect(reverse("user_login"))
       
@role_required(allowed_roles=["Admin"])
def employee_add(request):
    if request.session.get('user_id'):
        if request.method=="POST":
            user_form=UserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                return HttpResponseRedirect(reverse('employee:emp_list'))
            else:
                return render(request,'employee/add.html',context={"user_form":user_form})

        else:
            user_form=UserForm()
            return render(request,'employee/add.html',context={"user_form":user_form})
    return HttpResponseRedirect(reverse("user_login"))


def employee_edit(request,id):
    if request.role=="Admin":
        if request.session.get('user_id'):
            user=get_object_or_404(User,id=id)
            print(request.method)
            if request.method=="POST":
                user_form=UserForm(request.POST,instance=user)
                if user_form.is_valid():
                    user_form.save()
                    return HttpResponseRedirect(reverse('employee:emp_list'))
                else:
                    return render(request,'employee/edit.html',context={"user_form":user_form})
        
            else:
                user_form=UserForm(instance=user)
                return render(request,'employee/edit.html',context={"user_form":user_form})
        return HttpResponseRedirect(reverse("user_login"))
    return HttpResponseRedirect(reverse('employee:emp_list'))


def employee_delete(request,id):
    if request.session.get('user_id'):
        try:
            user=get_object_or_404(User,id=id)
        except User.DoesNotExist:
            print("User does not exist")
        else:
            user.delete()
        finally:
            return HttpResponseRedirect(reverse('employee:emp_list'))
    return HttpResponseRedirect(reverse("user_login"))
    
