from django.shortcuts import render,HttpResponse,Http404
from .models import Question,Choice,Answer



# Create your views here.

def index(request):
    questions=Question.objects.all()
    context={"questions":questions}
    return render(request,'poll/index.html',context)

def details(request,id):
    question=Question.objects.get(pk=id)
    context={"question":question}
    return render(request,'poll/details.html',context)

def poll(request,id=None):
    if request.method=="GET":
        context={}
        try:
            context['question']=Question.objects.get(id=id)
        except:
            raise Http404
        return render(request,'poll/poll.html',context=context)
    if request.method=="POST":
        user_id=1
        data=request.POST
        question=Choice.objects.get(id=data['choice']).question.id
        resp=Answer.objects.create(user_id=user_id,question_id=question,choice_id=data['choice'])
        if resp:
            return HttpResponse("Your vote is done successfully")
        else:
            return HttpResponse("Something went wrong")

            
        
from django.views.generic import View
from django.views.generic.edit import CreateView
from poll.models import *
from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from poll.forms import PollForm,ChoiceForm

class PollView(View):
    decorator=[login_required]

    @method_decorator(decorator)
    def get(self,request,id=None):
        if id:
            question=get_object_or_404(Question,id=id)
            poll_form=PollForm(instance=Question)
            choices=question.choice.set_all()
            choice_forms=[ChoiceForm(prefix=str(choice.id),instance=choice) for choice in choices]
            template='poll/edit_poll.html'
        else:
            poll_form=PollForm(instance=Question())
            choice_forms=[ChoiceForm(prefix=str(x),instance=Choice()) for x in range(3)]
            template='poll/new_poll.html'
        context={'poll_form':poll_form,'choice_forms':choice_forms}
        return render(request,template,context)


    @method_decorator(decorator)
    def post(self,request):
        context={}
        poll_form=PollForm(request.POST,instance=Question())
        choice_form=[ChoiceForm(request.POST,prefix=str(x),instance=Choice()) for x in range(3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_form]):
            new_poll=poll_form.save()
            new_poll.created_by=request.user
            new_poll.save()
            for cf in choice_form:
                new_choice=cf.save(commit=False)
                new_choice.question=new_poll
                new_choice.save()
            return HttpResponseRedirect('/polls/')
        context={'poll_form':poll_form,'choice_forms':choice_form}
        return render(request,'poll/new_poll.html',context)

    

