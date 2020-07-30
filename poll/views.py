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

            
        
